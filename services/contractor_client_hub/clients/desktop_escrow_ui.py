from __future__ import annotations

import os

import customtkinter as ctk
from pydantic import BaseModel, Field, ValidationError, field_validator
from web3 import Web3


class EscrowAgreement(BaseModel):
    client_address: str = Field(
        ..., min_length=42, max_length=42, description="Ethereum/Polygon address"
    )
    contractor_address: str = Field(..., min_length=42, max_length=42)
    usdt_amount: float = Field(..., gt=0, description="Must be greater than zero")
    deliverables_cid: str = Field(
        ..., min_length=46, description="IPFS CID containing AI deliverable bundle"
    )

    @field_validator("client_address", "contractor_address")
    @classmethod
    def address_hex_format(cls, v: str) -> str:
        if not v.startswith("0x"):
            raise ValueError("Address must start with 0x")
        return v


w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_RPC_URL", "https://polygon-rpc.com")))


class AIAssistedEscrowUI(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Decentralized AI Escrow Manager")
        self.geometry("600x540")
        ctk.set_appearance_mode("dark")

        self.label = ctk.CTkLabel(
            self, text="Draft New Escrow Agreement", font=("Arial", 22, "bold")
        )
        self.label.pack(pady=25)

        self.client_entry = ctk.CTkEntry(
            self, placeholder_text="Client Wallet Address (0x...)", width=500
        )
        self.client_entry.pack(pady=10)

        self.contractor_entry = ctk.CTkEntry(
            self, placeholder_text="Contractor Wallet Address (0x...)", width=500
        )
        self.contractor_entry.pack(pady=10)

        self.amount_entry = ctk.CTkEntry(self, placeholder_text="USDT Amount", width=500)
        self.amount_entry.pack(pady=10)

        self.ipfs_entry = ctk.CTkEntry(
            self, placeholder_text="Deliverables IPFS CID (e.g., Qm...)", width=500
        )
        self.ipfs_entry.pack(pady=10)

        self.submit_btn = ctk.CTkButton(
            self,
            text="Validate & Sign Locally",
            font=("Arial", 16, "bold"),
            command=self.secure_submit,
            fg_color="#10B981",
            hover_color="#059669",
        )
        self.submit_btn.pack(pady=30)

        self.status_label = ctk.CTkLabel(self, text="", font=("Arial", 14), wraplength=540)
        self.status_label.pack()

    def secure_submit(self) -> None:
        try:
            agreement = EscrowAgreement(
                client_address=self.client_entry.get().strip(),
                contractor_address=self.contractor_entry.get().strip(),
                usdt_amount=float(self.amount_entry.get()),
                deliverables_cid=self.ipfs_entry.get().strip(),
            )

            if not w3.is_address(agreement.client_address) or not w3.is_address(
                agreement.contractor_address
            ):
                raise ValueError("Invalid Web3 address.")

            if not w3.is_connected():
                self.status_label.configure(
                    text=(
                        "Validated locally. RPC not reachable right now; "
                        "you can still proceed with offline signing flow."
                    ),
                    text_color="#F59E0B",
                )
                return

            self.status_label.configure(
                text=(
                    f"Data validated. Ready to secure {agreement.usdt_amount} USDT on-chain. "
                    "Proceed with local key-signing from your keystore."
                ),
                text_color="#10B981",
            )
        except ValidationError:
            self.status_label.configure(
                text="Validation error: please check input formatting.",
                text_color="#EF4444",
            )
        except ValueError as exc:
            self.status_label.configure(text=f"Web3 error: {exc}", text_color="#EF4444")


if __name__ == "__main__":
    app = AIAssistedEscrowUI()
    app.mainloop()
