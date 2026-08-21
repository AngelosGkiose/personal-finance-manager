import argparse

from app.database.database import SessionLocal
from app.models import UserModel
from app.config_data.father_financial_profile import (
    FATHER_FINANCIAL_PROFILE,
)
from app.services.financial_profile_initialization_service import (
    initialize_financial_profile_service,
)


def main():
    parser = argparse.ArgumentParser(
        description="Initialize father's financial profile"
    )

    parser.add_argument(
        "--email",
        required=True,
        help="Email of the user whose financial profile will be initialized"
    )

    args = parser.parse_args()

    db = SessionLocal()

    try:
        current_user = (
            db.query(UserModel)
            .filter(
                UserModel.email == args.email
            )
            .first()
        )

        if not current_user:
            print(
                f"User with email '{args.email}' was not found."
            )
            return

        result = initialize_financial_profile_service(
            profile=FATHER_FINANCIAL_PROFILE,
            current_user=current_user,
            db=db
        )

        print("Financial profile initialized successfully.")
        print(
            f"Categories created: "
            f"{result.categories_created}"
        )
        print(
            f"Categorization rules created: "
            f"{result.categorization_rules_created}"
        )
        print(
            f"Recurring income rules created: "
            f"{result.recurring_income_rules_created}"
        )

    finally:
        db.close()


if __name__ == "__main__":
    main()