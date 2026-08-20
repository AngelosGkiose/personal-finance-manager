from datetime import date, datetime
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models.user_model import UserModel
from app.schemas.bank_transaction import BankAutomationResult
from app.services.bank_sync_service import sync_bank_transactions_service
from app.services.bank_transaction_processor_service import (
    process_incoming_bank_transactions_service,
    process_outgoing_bank_transactions_service,
)
from app.services.recurring_income_rule_service import (
    generate_expected_incomes_for_month_service,
)


def run_bank_automation_service(
    db: Session,
    current_user: UserModel,
    provider,
    run_date: date | None = None
) -> BankAutomationResult:

    target_date = (
        run_date
        if run_date
        else datetime.now(
            ZoneInfo("Europe/Athens")
        ).date()
    )

    generated_expected_incomes = (
        generate_expected_incomes_for_month_service(
            year=target_date.year,
            month=target_date.month,
            current_user=current_user,
            db=db
        )
    )

    sync_result = sync_bank_transactions_service(
        db=db,
        current_user=current_user,
        provider=provider
    )

    outgoing_result = (
        process_outgoing_bank_transactions_service(
            db=db,
            current_user=current_user
        )
    )

    incoming_result = (
        process_incoming_bank_transactions_service(
            db=db,
            current_user=current_user
        )
    )

    return BankAutomationResult(
        generated_expected_incomes=len(
            generated_expected_incomes
        ),
        transactions_received=sync_result.received,
        transactions_created=sync_result.created,
        transactions_skipped=sync_result.skipped,
        outgoing_found=outgoing_result.found,
        outgoing_processed=outgoing_result.processed,
        incoming_found=incoming_result.found,
        incoming_processed=incoming_result.processed
    )