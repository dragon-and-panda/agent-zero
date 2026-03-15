from __future__ import annotations

import time
import uuid

from .. import schemas


class EscrowAdapter:
    """Escrow state transition helper.

    This adapter simulates on-chain state while exposing fields needed
    for later smart-contract integration (tx hash, contract address, token/network).
    """

    def fund(
        self,
        thread: schemas.ContractThread,
        amount_usdt: float,
        tx_hash: str | None = None,
        contract_address: str | None = None,
    ) -> schemas.EscrowRecord:
        if amount_usdt <= 0:
            raise ValueError("Escrow amount must be positive.")
        if round(amount_usdt, 6) != round(thread.terms.amount_usdt, 6):
            raise ValueError("Funding amount must match contract amount.")
        escrow = thread.escrow
        if escrow.status not in (schemas.EscrowStatus.none,):
            raise ValueError("Escrow is already funded or finalized.")

        escrow.amount_usdt = float(amount_usdt)
        escrow.network = thread.terms.network
        escrow.token = thread.terms.token
        escrow.contract_address = contract_address or escrow.contract_address
        escrow.tx_hash = tx_hash or f"sim-{uuid.uuid4().hex}"
        escrow.funded_at = time.time()
        escrow.status = schemas.EscrowStatus.funded
        return escrow

    def release(
        self,
        thread: schemas.ContractThread,
        to_contractor_usdt: float,
        to_platform_usdt: float,
    ) -> schemas.EscrowRecord:
        escrow = thread.escrow
        if escrow.status not in (
            schemas.EscrowStatus.funded,
            schemas.EscrowStatus.partially_released,
            schemas.EscrowStatus.locked_dispute,
        ):
            raise ValueError("Escrow is not in releasable state.")
        if to_contractor_usdt < 0 or to_platform_usdt < 0:
            raise ValueError("Release amounts cannot be negative.")

        remaining = self.remaining_balance(thread)
        requested = to_contractor_usdt + to_platform_usdt
        if requested <= 0:
            raise ValueError("Release must disburse a positive amount.")
        if requested - remaining > 1e-9:
            raise ValueError("Release exceeds escrow balance.")

        escrow.released_to_contractor_usdt += float(to_contractor_usdt)
        escrow.released_to_platform_usdt += float(to_platform_usdt)

        if abs(self.remaining_balance(thread)) <= 1e-6:
            escrow.status = schemas.EscrowStatus.released
        else:
            escrow.status = schemas.EscrowStatus.partially_released
        return escrow

    def refund(self, thread: schemas.ContractThread, refund_to_client_usdt: float) -> schemas.EscrowRecord:
        escrow = thread.escrow
        if refund_to_client_usdt < 0:
            raise ValueError("Refund amount cannot be negative.")
        remaining = self.remaining_balance(thread)
        if refund_to_client_usdt - remaining > 1e-9:
            raise ValueError("Refund exceeds escrow balance.")
        escrow.refunded_to_client_usdt += float(refund_to_client_usdt)
        if abs(self.remaining_balance(thread)) <= 1e-6:
            escrow.status = schemas.EscrowStatus.refunded
        else:
            escrow.status = schemas.EscrowStatus.partially_released
        return escrow

    def lock_for_dispute(self, thread: schemas.ContractThread) -> schemas.EscrowRecord:
        if thread.escrow.status in (
            schemas.EscrowStatus.funded,
            schemas.EscrowStatus.partially_released,
        ):
            thread.escrow.status = schemas.EscrowStatus.locked_dispute
        return thread.escrow

    def remaining_balance(self, thread: schemas.ContractThread) -> float:
        escrow = thread.escrow
        used = (
            escrow.released_to_contractor_usdt
            + escrow.released_to_platform_usdt
            + escrow.refunded_to_client_usdt
        )
        return max(0.0, round(float(escrow.amount_usdt) - float(used), 6))
