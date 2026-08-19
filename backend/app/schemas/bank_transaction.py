from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.bank_transaction_model import BankTransactionDirection


class BankTransactionImport(BaseModel):
    external_transaction_id: str = Field(
        min_length=1,
        max_length=255
    )

    provider: str = Field(
        min_length=1,
        max_length=50
    )

    amount: Decimal = Field(
        gt=0
    )

    direction: BankTransactionDirection

    description: str = Field(
        min_length=1,
        max_length=255
    )

    transaction_date: date

    currency: str = Field(
        default="EUR",
        min_length=3,
        max_length=3
    )
class BankSyncResult(BaseModel):
    received: int
    created: int
    skipped: int

class BankTransactionProcessingResult(BaseModel):
    found: int
    processed: int