"""Offline documentation contracts, not live session/HTTP security tests."""
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate import validate


OWNERS = (
    "hcp-operations", "hcp-foundations", "hcp-connections", "hcp-alpha-data-collection",
    "hcp-trade-equipment", "hcp-customer-accounts", "hcp-jobs-history",
    "hcp-pricebook-procurement", "hcp-reference-configuration",
    "hcp-reporting-exports", "hcp-webhook-recovery",
)


class SessionGuidanceTests(unittest.TestCase):
    def test_standalone_copies_and_discovery(self):
        canonical = (ROOT / "docs/internal-session-workflow.md").read_bytes()
        index = (ROOT / "DOCUMENT_INDEX.md").read_text()
        for owner in OWNERS:
            with self.subTest(owner=owner):
                relative = f"skills/{owner}/references/internal-session-workflow.md"
                self.assertEqual((ROOT / relative).read_bytes(), canonical)
                self.assertIn(relative, index)
                entry = ROOT / f"skills/{owner}/SKILL.md"
                adapter = ROOT / f"skills/{owner}/references/adapters.md"
                self.assertIn("internal-session-workflow.md", entry.read_text() +
                              (adapter.read_text() if adapter.exists() else ""))
        for relative in ("README.md", "docs/adapters.md", "docs/MIGRATION.md"):
            self.assertIn("internal-session-workflow.md", (ROOT / relative).read_text())

    def test_decisions_and_negative_safety_contracts(self):
        text = (ROOT / "docs/internal-session-workflow.md").read_text()
        required = (
            "Use the supported public API when sufficient",
            "prefer a verified authorized Alpha/internal-session API over UI clicking",
            "secure login/MFA/session bootstrap", "visual verification",
            "missing secure HTTP/session capability", "per-tenant isolated session jars",
            "CSRF/header requirements", "allowed HTTPS host, method, path",
            "read back the authenticated account/company",
            "before collecting children or writing", "directory 0700, files 0600",
            "never request passwords, cookies or OTPs in chat",
            "Do not export raw HAR/storage-state files",
            "Do not claim that cookies alone suffice or that CSRF is never required",
            "Missing identity capability or a mismatch blocks work",
            "Disable automatic redirects", "fresh unauthenticated client",
            "obtain exact-operation authorization", "Submit once",
            "read back the exact operation's target", "reconciliation, not retry",
            "one bounded GET retry", "For 403/access denial, stop",
            "not an executable security boundary",
        )
        for phrase in required:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_missing_and_divergent_copy_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            tree = Path(temp) / "pack"
            shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            copy = tree / "skills/hcp-foundations/references/internal-session-workflow.md"
            copy.write_text("# Divergent instructions\n")
            self.assertIn("internal-session workflow copy drift", validate(tree))
            copy.unlink()
            self.assertIn("missing internal-session workflow copy", validate(tree))

    def test_missing_canonical_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            tree = Path(temp) / "pack"
            shutil.copytree(ROOT, tree, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            (tree / "docs/internal-session-workflow.md").unlink()
            self.assertIn("missing internal-session workflow", validate(tree))


if __name__ == "__main__":
    unittest.main()
