from datetime import date
from decimal import Decimal

from app.models.bank_transaction_model import BankTransactionDirection
from app.schemas.bank_transaction import BankTransactionImport


class FakeBankProvider:

    def get_transactions(self) -> list[BankTransactionImport]:
        return [
            BankTransactionImport(
                external_transaction_id="tx_001",
                provider="fake_bank",
                amount=Decimal("65.00"),
                direction=BankTransactionDirection.OUTGOING,
                description="SHELL KIFISIAS",
                transaction_date=date(2026, 8, 18),
                value_date=date(2026, 8, 17),
                currency="EUR"
            ),

            BankTransactionImport(
                external_transaction_id="tx_002",
                provider="fake_bank",
                amount=Decimal("1300.00"),
                direction=BankTransactionDirection.INCOMING,
                description="SALARY AUGUST",
                transaction_date=date(2026, 8, 18),
                value_date=date(2026, 8, 17),
                currency="EUR"
            ),

            BankTransactionImport(
                external_transaction_id="tx_003",
                provider="fake_bank",
                amount=Decimal("84.50"),
                direction=BankTransactionDirection.OUTGOING,
                description="SKLAVENITIS",
                transaction_date=date(2026, 8, 18),
                value_date=date(2026, 8, 17),
                currency="EUR"
            )
        ]