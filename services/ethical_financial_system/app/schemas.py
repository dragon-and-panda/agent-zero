from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ConsentStatus(str, Enum):
    unknown = "unknown"
    opted_in = "opted_in"
    transactional = "transactional"
    opted_out = "opted_out"
    do_not_contact = "do_not_contact"


class ContactSource(str, Enum):
    received = "received"
    sent = "sent"
    cc = "cc"
    bcc = "bcc"
    file_import = "file_import"
    manual = "manual"


class GmailHeaderMessage(BaseModel):
    message_id: str = Field(..., description="Provider-specific message identifier.")
    subject: Optional[str] = Field(None, description="Optional message subject metadata.")
    sent_at: Optional[str] = Field(None, description="Original sent time (ISO string if available).")
    from_addresses: List[str] = Field(default_factory=list)
    to_addresses: List[str] = Field(default_factory=list)
    cc_addresses: List[str] = Field(default_factory=list)
    bcc_addresses: List[str] = Field(default_factory=list)


class HeaderIngestionRequest(BaseModel):
    owner_id: str = Field(..., description="Data owner identifier.")
    owner_consent_asserted: bool = Field(
        ...,
        description="Must be true to proceed; confirms the owner authorized this ingestion.",
    )
    default_consent_status: ConsentStatus = ConsentStatus.unknown
    messages: List[GmailHeaderMessage] = Field(default_factory=list)


class CsvIngestionRequest(BaseModel):
    owner_id: str
    owner_consent_asserted: bool = Field(
        ...,
        description="Must be true to proceed; confirms the owner authorized this ingestion.",
    )
    csv_content: str = Field(..., description="Raw CSV text.")
    email_column: str = Field("email", description="Column name containing email addresses.")
    consent_column: Optional[str] = Field(
        None,
        description="Optional column with consent values (e.g., opted_in, opted_out).",
    )
    suppression_column: Optional[str] = Field(
        None, description="Optional boolean-like suppression flag column."
    )
    default_source: ContactSource = ContactSource.file_import
    default_consent_status: ConsentStatus = ConsentStatus.unknown


class ContactRecord(BaseModel):
    owner_id: str
    email: str
    consent_status: ConsentStatus
    suppression_flag: bool
    sources: List[str] = Field(default_factory=list)
    first_seen_at: float
    last_seen_at: float
    evidence_count: int
    last_source: Optional[str] = None


class IngestionSummary(BaseModel):
    processed_items: int
    unique_valid_addresses: int
    inserted: int
    updated: int
    invalid_addresses: int
    duplicate_addresses: int


class IngestionResponse(BaseModel):
    summary: IngestionSummary
    touched_contacts: List[ContactRecord] = Field(default_factory=list)
