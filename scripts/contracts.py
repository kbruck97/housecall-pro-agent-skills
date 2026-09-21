"""Offline policy contracts; no network, provider writes or credential handling."""
from decimal import Decimal, InvalidOperation
import hashlib
import hmac
import math
import re
from urllib.parse import urlsplit


def source_id(value, prefix="job"):
    """Validate this declared namespace; never strip/repair input."""
    if not isinstance(value, str) or not re.fullmatch(re.escape(prefix) + r"_[0-9a-fA-F]{32}", value):
        raise ValueError("invalid source identifier; preserve and clarify")
    return value


def auth_scheme(kind):
    if kind not in {"api-key", "oauth"}:
        raise ValueError("unknown credential type")
    return "Token" if kind == "api-key" else "Bearer"


def scope(row, company, customer, address=None):
    if not company or not customer or row.get("company_id") != company or row.get("customer_id") != customer:
        raise ValueError("tenant/customer mismatch")
    if address is not None and (address in ("", "0", 0) or row.get("address_id") != address or row.get("billing_only")):
        raise ValueError("service-property mismatch")
    return row


def collect_pages(pages, *, company, customer, nested=False):
    """Validate a completed synthetic envelope sequence, not a fetching client.

    Adapter must normalize endpoint envelopes to this contract; page_size/per_page
    differences are handled by pagination_parameter, not guessed from responses.
    """
    if not pages:
        raise ValueError("unqueried is not empty")
    result, seen = [], set()
    totals = None
    for expected, raw in enumerate(pages, 1):
        page = raw.get("data") if nested else raw
        if not isinstance(page, dict):
            raise ValueError("malformed envelope")
        count, last = page.get("total_items"), page.get("total_pages")
        if type(count) is not int or count < 0 or type(last) is not int or last < 1:
            raise ValueError("missing completeness metadata")
        if page.get("page") != expected or (totals is not None and totals != (count, last)):
            raise ValueError("repeated page or changing totals")
        totals = (count, last)
        if not isinstance(page.get("items"), list):
            raise ValueError("malformed items")
        for row in page["items"]:
            scope(row, company, customer)
            ident = row.get("id")
            if not isinstance(ident, str) or not ident or ident in seen:
                raise ValueError("missing/duplicate row identity")
            seen.add(ident)
            result.append(row)
    if totals is None or len(pages) != totals[1] or len(result) != totals[0]:
        raise ValueError("partial collection")
    return result


def pagination_parameter(resource):
    if resource == "routes":
        return "per_page"
    if resource in {"customers", "employees", "jobs", "estimates", "invoices", "events"}:
        return "page_size"
    raise ValueError("endpoint pagination unverified")


def reset_delay(epoch_header, now):
    try:
        epoch = float(epoch_header)
        if not (0 <= epoch < 10**12):
            raise ValueError
        return max(0.0, epoch - now)
    except (ValueError, TypeError):
        raise ValueError("invalid reset; use adapter bounded-backoff policy") from None


def allocated_total(lines):
    """No fallback to full amount: missing allocation is unresolved, not zero."""
    total = Decimal(0)
    for line in lines:
        raw = line.get("invoiced_amount")
        if raw is None or isinstance(raw, bool):
            raise ValueError("allocation unknown")
        try:
            amount = Decimal(str(raw))
        except InvalidOperation:
            raise ValueError("invalid allocation") from None
        if not amount.is_finite():
            raise ValueError("invalid allocation")
        total += amount
    return total


def equipment_decision(*, mode, completed, target_evidence, model=None, serial=None, proposed=False):
    """A candidate classification only, never permission to create equipment."""
    if mode not in {"installed-new", "serviced-existing"}:
        raise ValueError("explicit mode required")
    if proposed or not completed or not target_evidence:
        return "hold"
    if mode == "installed-new" and not (model and serial):
        return "hold"
    return "candidate"


def json_exact_equal(left, right):
    """Compare JSON values without coercion; int and float are distinct here.

    Only exact built-in JSON representations are accepted. Nonfinite floats,
    non-string object keys, custom types and cyclic/overdeep containers fail closed.
    Object order is immaterial; array order and nested key sets are exact.
    """
    def compare(a, b):
        kind = type(a)
        if kind is not type(b):
            return False
        if kind in (type(None), bool, int, str):
            return a == b
        if kind is float:
            return math.isfinite(a) and math.isfinite(b) and a == b
        if kind is list:
            return len(a) == len(b) and all(compare(x, y) for x, y in zip(a, b))
        if kind is dict:
            return (all(type(k) is str for k in a) and all(type(k) is str for k in b)
                    and a.keys() == b.keys() and all(compare(a[k], b[k]) for k in a))
        return False

    try:
        return compare(left, right)
    except RecursionError:
        return False


def mutation_verdict(plan, receipt=None, readback=None):
    """Fail-closed state evaluator for synthetic adapter integration plans."""
    if not isinstance(plan, dict):
        return "blocked"
    # Adapter-normalized opaque strings, not a universal HCP identifier grammar.
    identities = ("company_id", "customer_id", "address_id", "target_id", "intent_id", "before_digest", "operation")
    if any(not isinstance(plan.get(k), str) or not plan[k].strip() for k in identities):
        return "blocked"
    # Known invalid service-property sentinel; never repair or coerce an ID.
    if plan["address_id"] == "0":
        return "blocked"
    if (type(plan.get("expected")) is not dict or not plan["expected"]
            or not json_exact_equal(plan["expected"], plan["expected"])):
        return "blocked"
    approved = plan.get("approved_operations")
    if not isinstance(approved, (list, tuple, set, frozenset)) or not approved:
        return "blocked"
    if any(not isinstance(operation, str) or not operation.strip() for operation in approved):
        return "blocked"
    if plan["operation"] not in approved:
        return "blocked"
    if plan.get("authorized") is not True or plan.get("dry_run") is not False:
        return "dry-run"
    if plan.get("current_digest") != plan["before_digest"] or plan.get("coverage_complete") is not True:
        return "blocked"
    if receipt is None:
        return "awaiting-execution"
    if not isinstance(receipt, dict) or not isinstance(receipt.get("status"), str):
        return "blocked"
    if receipt.get("status") in {"timeout", "unknown"}:
        return "ambiguous-reconcile-no-retry"
    if receipt.get("status") != "accepted" or receipt.get("intent_id") != plan["intent_id"]:
        return "blocked"
    if not isinstance(readback, dict):
        return "unverified"
    if any(readback.get(k) != plan[k] for k in ("company_id", "customer_id", "address_id", "target_id")):
        return "unverified"
    return "verified" if all(k in readback and json_exact_equal(readback[k], v) for k, v in plan["expected"].items()) else "unverified"


def attachment_request(url, allowed_hosts, headers=None, redirect=False):
    """Validate an unauthenticated HTTPS request; downloader must enforce DNS/IP policy too."""
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.username or parsed.password or parsed.hostname not in allowed_hosts or parsed.port not in (None, 443):
        raise ValueError("untrusted attachment destination")
    if headers or redirect:
        raise ValueError("fresh unauthenticated client; redirects require new validation")
    return {"headers": {}, "follow_redirects": False}


def verify_webhook(secret, timestamp, body, signature_hex, *, now, tolerance=300):
    """Pure HMAC check. Caller parses actual header format and durably dedupes events.

    tolerance is local policy, not an asserted HCP delivery SLA.
    """
    if not isinstance(body, bytes) or not isinstance(timestamp, str) or not timestamp.isdigit():
        return False
    if tolerance < 0 or abs(now - int(timestamp)) > tolerance:
        return False
    if not isinstance(signature_hex, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", signature_hex):
        return False
    expected = hmac.new(secret, timestamp.encode() + b"." + body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature_hex.lower())


def send_gate(context):
    """Normalized consent/ownership preflight only; caller must serialize check+send.

    Unknown consent or missing durable consent lookup fails closed. This does not
    interpret customer language or perform suppression persistence.
    """
    required_true = ("tenant_bound", "endpoint_verified", "consent_lookup_ok", "purpose_allowed",
                     "owner_verified", "source_fresh", "send_authorized", "quiet_hours_ok")
    if any(context.get(key) is not True for key in required_true):
        return "blocked"
    if context.get("global_dnc") is not False or context.get("wrong_number") is not False:
        return "suppressed"
    if context.get("workflow_closed") is not False or context.get("complaint_pending") is not False:
        return "hold"
    return "eligible-not-sent"


def paired_receipt(records):
    """Count verified record writes, not inferred physical units or HTTP accepts."""
    statuses = [row.get("status") for row in records]
    return {"verified_record_writes": statuses.count("verified"),
            "state": "verified" if statuses and all(s == "verified" for s in statuses) else "partial-or-unverified"}


def claim_allowed(kind, receipt):
    """Synthetic receipt check, not a natural-language consent classifier."""
    states = {"booked": "booking-verified", "paid": "payment-reconciled", "handed-off": "handoff-persisted", "sent": "delivery-accepted"}
    return kind in states and isinstance(receipt, dict) and receipt.get("state") == states[kind] and bool(receipt.get("target_id")) and bool(receipt.get("receipt_id"))
