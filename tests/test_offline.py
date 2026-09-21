"""Synthetic unit/security/contract tests. No real records or network."""
import hashlib
import hmac
import io
import json
from pathlib import Path
import shutil
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import contracts as c
import package as pack
import validate as v


class Contracts(unittest.TestCase):
    def test_literal_identifier_no_repair(self):
        good = "job_" + "a" * 32
        self.assertEqual(c.source_id(good), good)
        for bad in [good + " ", " " + good, good[:-1], 123, "display-12"]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                c.source_id(bad)

    def test_auth_and_endpoint_pagination(self):
        self.assertEqual(c.auth_scheme("api-key"), "Token")
        self.assertEqual(c.auth_scheme("oauth"), "Bearer")
        self.assertEqual(c.pagination_parameter("routes"), "per_page")
        self.assertEqual(c.pagination_parameter("jobs"), "page_size")
        with self.assertRaises(ValueError):
            c.pagination_parameter("equipment")
        with self.assertRaises(ValueError):
            c.auth_scheme("private-session")
        self.assertEqual(c.reset_delay("1200", 1000), 200)
        self.assertEqual(c.reset_delay("900", 1000), 0)
        for bad in [None, "not-epoch", "nan", "inf"]:
            with self.assertRaises(ValueError):
                c.reset_delay(bad, 1000)

    def pages(self):
        return [{"page": i, "total_pages": 2, "total_items": 2,
                 "items": [{"id": f"synthetic-{i}", "company_id": "tenant-A", "customer_id": "party-A"}]}
                for i in [1, 2]]

    def test_complete_and_nested_pages(self):
        for nested in [False, True]:
            pages = self.pages()
            if nested:
                pages = [{"data": x} for x in pages]
            self.assertEqual(len(c.collect_pages(pages, company="tenant-A", customer="party-A", nested=nested)), 2)
        empty = [{"page": 1, "total_pages": 1, "total_items": 0, "items": []}]
        self.assertEqual(c.collect_pages(empty, company="tenant-A", customer="party-A"), [])

    def test_partial_repeated_changed_ignored_filter(self):
        cases = [[], self.pages()[:1], self.pages() * 2]
        changed = self.pages(); changed[1]["total_items"] = 3; cases.append(changed)
        wrong = self.pages(); wrong[0]["items"][0]["customer_id"] = "party-B"; cases.append(wrong)
        duplicate = self.pages(); duplicate[1]["items"][0]["id"] = "synthetic-1"; cases.append(duplicate)
        malformed = self.pages(); malformed[0]["items"] = {}; cases.append(malformed)
        for pages in cases:
            with self.subTest(pages=pages), self.assertRaises(ValueError):
                c.collect_pages(pages, company="tenant-A", customer="party-A")

    def test_property_scope_and_billing_placeholder(self):
        row = {"company_id": "tenant-A", "customer_id": "party-A", "address_id": "property-A"}
        self.assertEqual(c.scope(row, "tenant-A", "party-A", "property-A"), row)
        for address in ["property-B", "0", 0, ""]:
            with self.assertRaises(ValueError):
                c.scope(row, "tenant-A", "party-A", address)
        row["billing_only"] = True
        with self.assertRaises(ValueError):
            c.scope(row, "tenant-A", "party-A", "property-A")
        with self.assertRaises(ValueError):
            c.scope(row, "tenant-B", "party-A")

    def test_split_allocation_not_full_amount(self):
        rows = [{"amount": 100, "invoiced_amount": "40"}, {"amount": 100, "invoiced_amount": "60"}]
        self.assertEqual(c.allocated_total(rows), 100)
        for missing in [None, True, "NaN", "Infinity", "bad"]:
            with self.assertRaises(ValueError):
                c.allocated_total([{"amount": 100, "invoiced_amount": missing}])

    def test_equipment_modes_are_not_interchangeable(self):
        args = {"completed": True, "target_evidence": True}
        self.assertEqual(c.equipment_decision(mode="serviced-existing", **args), "candidate")
        self.assertEqual(c.equipment_decision(mode="installed-new", **args), "hold")
        self.assertEqual(c.equipment_decision(mode="installed-new", model="SYN-M", serial="SYN-S", **args), "candidate")
        self.assertEqual(c.equipment_decision(mode="serviced-existing", proposed=True, **args), "hold")
        with self.assertRaises(ValueError):
            c.equipment_decision(mode="guess", **args)

    def plan(self):
        return {"company_id": "tenant-A", "customer_id": "party-A", "address_id": "property-A",
                "target_id": "synthetic-target", "operation": "schedule-update", "intent_id": "synthetic-intent",
                "before_digest": "synthetic-before", "current_digest": "synthetic-before", "expected": {"state": "scheduled"},
                "authorized": True, "dry_run": False, "approved_operations": ["schedule-update"], "coverage_complete": True}

    def test_mutation_authorization_ambiguity_and_readback(self):
        p = self.plan()
        receipt = {"status": "accepted", "intent_id": p["intent_id"]}
        row = {k: p[k] for k in ["company_id", "customer_id", "address_id", "target_id"]}
        row["state"] = "scheduled"
        self.assertEqual(c.mutation_verdict(p), "awaiting-execution")
        self.assertEqual(c.mutation_verdict(p, receipt), "unverified")
        self.assertEqual(c.mutation_verdict(p, receipt, row), "verified")
        self.assertEqual(c.mutation_verdict(p, {"status": "timeout"}), "ambiguous-reconcile-no-retry")
        for key, value, expected in [("authorized", False, "dry-run"), ("dry_run", True, "dry-run"), ("approved_operations", [], "blocked"), ("current_digest", "stale", "blocked"), ("coverage_complete", False, "blocked")]:
            q = dict(p); q[key] = value
            self.assertEqual(c.mutation_verdict(q, receipt, row), expected)
        row["address_id"] = "property-B"
        self.assertEqual(c.mutation_verdict(p, receipt, row), "unverified")
        receipt["intent_id"] = "unrelated"
        self.assertEqual(c.mutation_verdict(p, receipt, row), "blocked")

    def test_mutation_requires_typed_exact_operation_collection(self):
        for approved in [None, True, 1, "schedule-update", "prefix-schedule-update-suffix",
                         {"schedule-update": True}, [], ["prefix-schedule-update-suffix"],
                         ["schedule-update", None], ["schedule-update", 1],
                         ["schedule-update", ""], ["schedule-update", "  "]]:
            with self.subTest(approved=approved):
                self.assertEqual(c.mutation_verdict(dict(self.plan(), approved_operations=approved)), "blocked")
        for operation in [None, False, 1, [], {}, "", "  ", "schedule", "schedule-update "]:
            with self.subTest(operation=operation):
                self.assertEqual(c.mutation_verdict(dict(self.plan(), operation=operation)), "blocked")
        for collection in (list, tuple, set, frozenset):
            with self.subTest(collection=collection):
                self.assertEqual(c.mutation_verdict(dict(self.plan(), approved_operations=collection(["schedule-update"]))), "awaiting-execution")

    def test_mutation_rejects_invalid_scoped_identities(self):
        for key in ("company_id", "customer_id", "address_id", "target_id", "intent_id", "before_digest"):
            for value in (None, False, True, 0, 1, "", " \t", [], ["synthetic"], {}, {"id": "synthetic"}):
                with self.subTest(key=key, value=value):
                    self.assertEqual(c.mutation_verdict(dict(self.plan(), **{key: value})), "blocked")
        self.assertEqual(c.mutation_verdict(dict(self.plan(), address_id="0")), "blocked")
        for malformed in (None, [], "plan", 1):
            self.assertEqual(c.mutation_verdict(malformed), "blocked")

    def test_mutation_scoped_success_and_each_readback_mismatch(self):
        p = self.plan()
        # Opaque adapter identities need not match the source_id namespace grammar.
        p.update(company_id="tenant:synthetic", customer_id="party/synthetic",
                 address_id="property.synthetic", target_id="target-synthetic")
        receipt = {"status": "accepted", "intent_id": p["intent_id"]}
        row = {k: p[k] for k in ("company_id", "customer_id", "address_id", "target_id")}
        row.update(p["expected"])
        self.assertEqual(c.mutation_verdict(p, receipt, row), "verified")
        for key in row:
            with self.subTest(key=key):
                self.assertEqual(c.mutation_verdict(p, receipt, dict(row, **{key: "other"})), "unverified")
        for malformed in (False, True, 0, 1, "", "accepted", [], ["accepted"], {},
                          {"status": []}, {"status": {}}):
            self.assertEqual(c.mutation_verdict(p, malformed, row), "blocked")

    def test_mutation_json_type_exact_readback(self):
        pairs = [(True, 1), (False, 0), (1, 1.0), ("1", 1),
                 ({"enabled": True}, {"enabled": 1}),
                 ([False], [0]), ({"items": [True]}, {"items": [1]}),
                 ([1, 2], [2, 1]), ({"a": 1}, {"a": 1, "b": 2})]
        for expected, actual in pairs + [(b, a) for a, b in pairs]:
            with self.subTest(expected=expected, actual=actual):
                p = dict(self.plan(), expected={"value": expected})
                receipt = {"status": "accepted", "intent_id": p["intent_id"]}
                row = dict(p, value=actual)
                self.assertEqual(c.mutation_verdict(p, receipt, row), "unverified")
        for value in [None, True, False, 0, 1, 1.0, "1", [], {},
                      {"items": [True, False, None, 0, 1.0, {"name": "synthetic"}]}]:
            with self.subTest(value=value):
                p = dict(self.plan(), expected={"value": value})
                receipt = {"status": "accepted", "intent_id": p["intent_id"]}
                self.assertEqual(c.mutation_verdict(p, receipt, dict(p, value=json.loads(json.dumps(value)))), "verified")
        p = dict(self.plan(), expected={"value": {"a": 1, "b": False}})
        receipt = {"status": "accepted", "intent_id": p["intent_id"]}
        self.assertEqual(c.mutation_verdict(p, receipt, dict(p, value={"b": False, "a": 1})), "verified")

    def test_mutation_rejects_non_json_values(self):
        class IntegerSubclass(int):
            pass

        cycle = []; cycle.append(cycle)
        invalid = [float("nan"), float("inf"), float("-inf"), (1,), {1},
                   b"text", object(), {1: "value"}, IntegerSubclass(1), cycle]
        for value in invalid:
            for nested in (value, {"items": [value]}):
                with self.subTest(kind=type(value).__name__):
                    self.assertFalse(c.json_exact_equal(nested, nested))
                    p = dict(self.plan(), expected={"value": nested})
                    self.assertEqual(c.mutation_verdict(p), "blocked")
                    p = dict(self.plan(), expected={"value": None})
                    receipt = {"status": "accepted", "intent_id": p["intent_id"]}
                    self.assertEqual(c.mutation_verdict(p, receipt, dict(p, value=nested)), "unverified")

    def test_adapter_references_preserve_historical_route_limits(self):
        canonical = (ROOT / "docs/adapters.md").read_text()
        copies = sorted((ROOT / "skills").glob("*/references/adapters.md"))
        self.assertEqual(len(copies), 7)
        for path in [ROOT / "docs/adapters.md", *copies]:
            text = path.read_text()
            with self.subTest(path=path):
                self.assertEqual(text.split("## Required request boundary", 1)[1],
                                 canonical.split("## Required request boundary", 1)[1])
                self.assertIn("non-executable design references only", text)
                self.assertIn("explicit opt-in", text)
                self.assertNotIn("Detailed internal routes are intentionally omitted", text)
                self.assertNotIn("no portable private routes", text)
        historical = (ROOT / "skills/hcp-trade-equipment/references/guarded-mutations.md").read_text()
        self.assertIn("non-executable historical evidence", historical)
        self.assertIn("current operation/schema/security verification", historical)
        self.assertIn("POST /alpha/equipment", historical)

    def test_happy_call_lifecycle_contract_retains_final_touch_assertions(self):
        # Documentation regression only: no scanner/sender implementation is shipped.
        text = (ROOT / "skills/hcp-happy-calls/references/adapter-and-evidence-contract.md").read_text()
        for assertion in ("Require each configured intended attempt to become eligible",
                          "terminal status/outcome", "cleared or neutralized due date",
                          "Scanner cap blocks a configured later attempt",
                          "Final touch leaves an active status or live due date"):
            with self.subTest(assertion=assertion):
                self.assertIn(assertion, text)

    def test_attachment_isolation_and_redirects(self):
        url = "https://media.example.org/synthetic-image"
        self.assertEqual(c.attachment_request(url, {"media.example.org"}), {"headers": {}, "follow_redirects": False})
        for kwargs in [{"headers": {"Authorization": "placeholder"}}, {"headers": {"Cookie": "placeholder"}}, {"redirect": True}]:
            with self.assertRaises(ValueError):
                c.attachment_request(url, {"media.example.org"}, **kwargs)
        for bad in ["http://media.example.org/file", "https://other.example.org/file", "https://media.example.org:444/file"]:
            with self.assertRaises(ValueError):
                c.attachment_request(bad, {"media.example.org"})

    def test_webhook_raw_bytes_timing_and_signature(self):
        secret, timestamp, body = b"synthetic-test-only", "1000", b'{"synthetic": true}'
        sig = hmac.new(secret, timestamp.encode() + b"." + body, hashlib.sha256).hexdigest()
        self.assertTrue(c.verify_webhook(secret, timestamp, body, sig, now=1000))
        self.assertFalse(c.verify_webhook(secret, timestamp, body.replace(b" ", b""), sig, now=1000))
        self.assertFalse(c.verify_webhook(secret, timestamp, body, sig, now=1400))
        self.assertFalse(c.verify_webhook(secret, timestamp, body, "x" * 64, now=1000))
        self.assertFalse(c.verify_webhook(secret, "bad", body, sig, now=1000))

    def test_durable_consent_wrong_number_and_owner_gate(self):
        context = {k: True for k in ("tenant_bound", "endpoint_verified", "consent_lookup_ok", "purpose_allowed", "owner_verified", "source_fresh", "send_authorized", "quiet_hours_ok")}
        context.update({"global_dnc": False, "wrong_number": False, "workflow_closed": False, "complaint_pending": False})
        self.assertEqual(c.send_gate(context), "eligible-not-sent")
        for key in ("consent_lookup_ok", "owner_verified", "send_authorized", "source_fresh"):
            changed = dict(context); changed[key] = False
            self.assertEqual(c.send_gate(changed), "blocked")
        for key in ("global_dnc", "wrong_number"):
            changed = dict(context); changed[key] = True
            self.assertEqual(c.send_gate(changed), "suppressed")
        context["complaint_pending"] = True
        self.assertEqual(c.send_gate(context), "hold")

    def test_paired_store_partial_write_is_not_two_verified_records(self):
        result = c.paired_receipt([{"status": "verified"}, {"status": "accepted"}])
        self.assertEqual(result, {"verified_record_writes": 1, "state": "partial-or-unverified"})
        self.assertEqual(c.paired_receipt([])["state"], "partial-or-unverified")
        self.assertEqual(c.paired_receipt([{"status": "verified"}, {"status": "verified"}])["verified_record_writes"], 2)

    def test_receipt_claims_not_customer_statements(self):
        for kind in ["booked", "paid", "handed-off", "sent"]:
            self.assertFalse(c.claim_allowed(kind, {"customer_said": "yes"}))
        self.assertTrue(c.claim_allowed("paid", {"state": "payment-reconciled", "target_id": "synthetic-invoice", "receipt_id": "synthetic-receipt"}))
        self.assertFalse(c.claim_allowed("booked", {"state": "handoff-persisted", "target_id": "synthetic-job", "receipt_id": "synthetic-receipt"}))


class Distribution(unittest.TestCase):
    def test_public_mit_license_and_private_export_boundary(self):
        self.assertIn("MIT License", (ROOT / "LICENSE").read_text())
        selected = {p.relative_to(ROOT).as_posix() for p in v.distribution_files(ROOT)}
        self.assertNotIn("docs/PLAN.md", selected)
        self.assertFalse(any(p.startswith("branch-start/") for p in selected))
        self.assertIn("docs/DISTRIBUTION.md", selected)
        for path in (ROOT / "skills").glob("*/SKILL.md"):
            self.assertEqual(v.frontmatter(path.read_text())["license"], "MIT")
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            (root / "LICENSE").write_text("All rights reserved")
            self.assertIn("invalid MIT license", v.validate(root))
        with self.assertRaises(ValueError):
            v.frontmatter("---\nname: synthetic\ndescription: example\nversion: 1\nlicense: Proprietary\n---\n")

    def test_excluded_internal_member_rejected_at_stage(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            archive = temp / "internal.tar"
            with tarfile.open(archive, "w") as tar:
                info = tarfile.TarInfo("docs/PLAN.md")
                info.size = 1
                tar.addfile(info, io.BytesIO(b"x"))
            with self.assertRaisesRegex(ValueError, "excluded internal"):
                pack.stage(archive, temp / "stage")
            self.assertFalse((temp / "stage").exists())

    def test_valid_repository(self):
        self.assertEqual(v.validate(ROOT), [])

    def test_root_adapter_required_and_indexed(self):
        self.assertIn("[AGENTS.md](AGENTS.md)", (ROOT / "DOCUMENT_INDEX.md").read_text())
        self.assertIn(ROOT / "AGENTS.md", v.distribution_files(ROOT))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            (root / "AGENTS.md").unlink()
            self.assertIn("missing AGENTS.md", v.validate(root))
            with self.assertRaises(ValueError):
                pack.build(root, Path(temp) / "missing-adapter.tar")

    def test_deliberate_invalid_fixtures(self):
        changes = {
            "frontmatter": ("skills/hcp-operations/SKILL.md", "broken"),
            "missing-link": ("docs/invalid.md", "[missing](not-present.md)"),
            "secret": ("docs/invalid.md", "-----BEGIN " + "PRIVATE KEY-----"),
            "private-home": ("docs/invalid.md", "/home/" + "synthetic-owner/private"),
            "missing-dependency": ("scripts/invalid.py", "import unavailable_dependency_xyz"),
            "source-coverage": ("docs/source-disposition.json", '{"families": []}'),
            "capability-source": ("docs/capabilities.json", '{"operations": [{"operation": "x", "status": "official-public"}], "status_definitions": {"official-public":"x"}}'),
        }
        for label, (relative, content) in changes.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temp:
                root = Path(temp) / "repo"
                shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
                (root / relative).write_text(content)
                self.assertTrue(v.validate(root), label)

    def test_duplicate_name_and_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            shutil.copytree(ROOT, root, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            shutil.copytree(root / "skills/hcp-operations", root / "skills/duplicate")
            self.assertTrue(any("duplicate" in e for e in v.validate(root)))
            (root / "docs/symlink").symlink_to(root / "LICENSE")
            self.assertTrue(any("symlink" in e for e in v.validate(root)))

    def test_reproducible_archive_and_stage(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            one = pack.build(ROOT, temp / "one.tar")
            two = pack.build(ROOT, temp / "two.tar")
            self.assertEqual(one["sha256"], two["sha256"])
            receipt = pack.stage(temp / "one.tar", temp / "staged")
            self.assertEqual(receipt["skills"], len(v.REQUIRED_SKILLS))
            self.assertEqual(v.validate(temp / "staged"), [])
            adapter = (ROOT / "AGENTS.md").read_bytes()
            self.assertEqual((temp / "staged/AGENTS.md").read_bytes(), adapter)
            manifest = json.loads((temp / "staged/PACKAGE_MANIFEST.json").read_text())
            self.assertEqual(manifest["AGENTS.md"], hashlib.sha256(adapter).hexdigest())
            self.assertFalse((temp / "staged/branch-start").exists())
            self.assertFalse((temp / "staged/.git").exists())
            with self.assertRaises(ValueError):
                pack.stage(temp / "one.tar", temp / "staged")
            with self.assertRaises(ValueError):
                pack.build(ROOT, temp / "one.tar")

    def test_unsafe_destination_and_tar(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            (temp / "alias").symlink_to(temp, target_is_directory=True)
            for path in [Path("relative"), temp / ".." / "bad", temp / "alias" / "bad"]:
                with self.assertRaises(ValueError):
                    pack.safe_new_path(path)
            for i, name in enumerate(["../escape", "/absolute", "a/../escape", "skills/link", "unexpected/file", "skills/back\\slash"]):
                archive = temp / f"unsafe-{i}.tar"
                with tarfile.open(archive, "w") as tar:
                    info = tarfile.TarInfo(name)
                    if name.endswith("link"):
                        info.type = tarfile.SYMTYPE; info.linkname = "../outside"
                        tar.addfile(info)
                    else:
                        info.size = 1; tar.addfile(info, io.BytesIO(b"x"))
                with self.assertRaises((ValueError, FileNotFoundError)):
                    pack.stage(archive, temp / f"out-{i}")
                self.assertFalse((temp / f"out-{i}").exists())


if __name__ == "__main__":
    unittest.main()
