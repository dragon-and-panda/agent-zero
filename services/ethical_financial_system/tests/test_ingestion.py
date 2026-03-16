import tempfile
import unittest

from app.schemas import (
    ConsentStatus,
    CsvIngestionRequest,
    GmailHeaderMessage,
    HeaderIngestionRequest,
)
from app.services.ingestion import ContactIngestionService
from app.services.normalization import normalize_email
from app.services.store import ContactStore


class IngestionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=True)
        self.store = ContactStore(self.tmp.name)
        self.service = ContactIngestionService(self.store)

    def tearDown(self) -> None:
        self.tmp.close()

    def test_normalize_email(self) -> None:
        self.assertEqual(normalize_email("Alice <ALICE@Example.com>"), "alice@example.com")
        self.assertEqual(normalize_email("mailto:bob@example.com"), "bob@example.com")
        self.assertIsNone(normalize_email("not-an-email"))

    def test_headers_require_consent_assertion(self) -> None:
        payload = HeaderIngestionRequest(
            owner_id="owner_1",
            owner_consent_asserted=False,
            messages=[
                GmailHeaderMessage(
                    message_id="msg-1",
                    from_addresses=["alice@example.com"],
                    to_addresses=["bob@example.com"],
                )
            ],
        )
        with self.assertRaises(PermissionError):
            self.service.ingest_headers(payload)

    def test_header_ingestion_dedup_and_invalid(self) -> None:
        payload = HeaderIngestionRequest(
            owner_id="owner_1",
            owner_consent_asserted=True,
            default_consent_status=ConsentStatus.opted_in,
            messages=[
                GmailHeaderMessage(
                    message_id="msg-1",
                    from_addresses=["Alice <ALICE@example.com>", "invalid@@example"],
                    to_addresses=["alice@example.com"],
                    cc_addresses=["carol@example.com"],
                )
            ],
        )
        summary, touched = self.service.ingest_headers(payload)

        self.assertEqual(summary.processed_items, 1)
        self.assertEqual(summary.unique_valid_addresses, 2)
        self.assertEqual(summary.invalid_addresses, 1)
        self.assertGreaterEqual(summary.inserted, 2)
        self.assertIn("alice@example.com", touched)
        self.assertIn("carol@example.com", touched)

    def test_csv_ingestion_consent_escalation_and_suppression(self) -> None:
        csv_content = (
            "email,consent,suppressed\n"
            "bob@example.com,opted_in,0\n"
            "BOB@example.com,opted_out,1\n"
            "carol@example.com,unknown,0\n"
        )
        payload = CsvIngestionRequest(
            owner_id="owner_2",
            owner_consent_asserted=True,
            csv_content=csv_content,
            email_column="email",
            consent_column="consent",
            suppression_column="suppressed",
        )
        summary, _ = self.service.ingest_csv(payload)
        self.assertEqual(summary.processed_items, 3)
        self.assertEqual(summary.unique_valid_addresses, 2)
        self.assertEqual(summary.duplicate_addresses, 1)

        contacts = self.store.list_contacts(owner_id="owner_2", limit=10)
        by_email = {c.email: c for c in contacts}
        bob = by_email["bob@example.com"]
        self.assertEqual(bob.consent_status, ConsentStatus.opted_out.value)
        self.assertTrue(bob.suppression_flag)
        self.assertEqual(bob.evidence_count, 2)


if __name__ == "__main__":
    unittest.main()
