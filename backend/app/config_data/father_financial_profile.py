from decimal import Decimal

from app.schemas.financial_profile import (
    CategorizationRuleSeed,
    FinancialProfileSeed,
    RecurringIncomeRuleSeed,
)


FATHER_FINANCIAL_PROFILE = FinancialProfileSeed(
    categories=[
        "Bills",
        "Subscriptions",
        "Shopping",
        "Food & Coffee",
        "Health",
        "Transport",
        "Cash Withdrawal",
        "Transfers",
        "Loan Payments",
        "Insurance",
        "Housing",
        "Home & Household",
        "Car Maintenance",
        "Bank Fees",
        "Taxes & Government",
        "Travel",
        "Services",
    ],

    categorization_rules=[
        # -------------------------------------------------
        # Supermarket
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="SKLAVENITIS",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="AB_",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="AB VASILOPOULOS",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="LIDL",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="MY MARKET",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="AZARIS",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="THIRAIKA MARKET",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="MASOUTIS",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="ΜΑΣΟΥΤΗΣ",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="GALAXIAS",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="ΓΑΛΑΞΙΑΣ",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="KRITIKOS",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="ΚΡΗΤΙΚΟΣ",
            category_name="Supermarket"
        ),
        CategorizationRuleSeed(
            keyword="BAZAAR",
            category_name="Supermarket"
        ),

        # -------------------------------------------------
        # Fuel
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="SHELL",
            category_name="Fuel"
        ),
        CategorizationRuleSeed(
            keyword="EKO",
            category_name="Fuel"
        ),
        CategorizationRuleSeed(
            keyword="TSAKONA",
            category_name="Fuel"
        ),
        CategorizationRuleSeed(
            keyword="SUPER FUELS",
            category_name="Fuel"
        ),
        CategorizationRuleSeed(
            keyword="AVIN",
            category_name="Fuel"
        ),
        CategorizationRuleSeed(
            keyword="ELIN",
            category_name="Fuel"
        ),
        CategorizationRuleSeed(
            keyword="REVOIL",
            category_name="Fuel"
        ),
        CategorizationRuleSeed(
            keyword="BP",
            category_name="Fuel"
        ),

        # -------------------------------------------------
        # Electricity
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="PROTERGIA",
            category_name="Electricity"
        ),
        CategorizationRuleSeed(
            keyword="DEI",
            category_name="Electricity"
        ),
        CategorizationRuleSeed(
            keyword="ΔΕΗ",
            category_name="Electricity"
        ),
        CategorizationRuleSeed(
            keyword="PPC",
            category_name="Electricity"
        ),
        CategorizationRuleSeed(
            keyword="HERON",
            category_name="Electricity"
        ),
        CategorizationRuleSeed(
            keyword="ΗΡΩΝ",
            category_name="Electricity"
        ),
        CategorizationRuleSeed(
            keyword="NRG",
            category_name="Electricity"
        ),
        CategorizationRuleSeed(
            keyword="ELPEDISON",
            category_name="Electricity"
        ),
        CategorizationRuleSeed(
            keyword="ZENITH",
            category_name="Electricity"
        ),
        CategorizationRuleSeed(
            keyword="ΖΕΝΙΘ",
            category_name="Electricity"
        ),

        # -------------------------------------------------
        # Water
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="EYDAP",
            category_name="Water"
        ),

        # -------------------------------------------------
        # Telecom
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="VODAFONE",
            category_name="Telecom"
        ),
        CategorizationRuleSeed(
            keyword="COSMOTE",
            category_name="Telecom"
        ),
        CategorizationRuleSeed(
            keyword="NOVA",
            category_name="Telecom"
        ),

        # -------------------------------------------------
        # Bills
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="ΕΝΤΠΛ",
            category_name="Bills"
        ),

        # -------------------------------------------------
        # Subscriptions
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="SPOTIFY",
            category_name="Subscriptions"
        ),
        CategorizationRuleSeed(
            keyword="APPLE.COM/BILL",
            category_name="Subscriptions"
        ),
        CategorizationRuleSeed(
            keyword="NETFLIX",
            category_name="Subscriptions"
        ),
        CategorizationRuleSeed(
            keyword="DISNEY",
            category_name="Subscriptions"
        ),
        CategorizationRuleSeed(
            keyword="DISNEYPLUS",
            category_name="Subscriptions"
        ),
        CategorizationRuleSeed(
            keyword="PRIME VIDEO",
            category_name="Subscriptions"
        ),
        CategorizationRuleSeed(
            keyword="YOUTUBE PREMIUM",
            category_name="Subscriptions"
        ),
        CategorizationRuleSeed(
            keyword="MICROSOFT",
            category_name="Subscriptions"
        ),
        CategorizationRuleSeed(
            keyword="GOOGLE ONE",
            category_name="Subscriptions"
        ),
        CategorizationRuleSeed(
            keyword="DROPBOX",
            category_name="Subscriptions"
        ),

        # -------------------------------------------------
        # Shopping
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="TEMU.COM",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="ALIEXPRESS",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="JUMBO",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="NIKE",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="ADIDAS",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="TSAKIRIS",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="HONDOS CENTER",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="DANAOS",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="SILVER SPORTS",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="ENTICON SHOPS",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="NAVY AND GREEN",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="GEORGIOPOULOI",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="ZARA",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="H&M",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="BERSHKA",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="PULL&BEAR",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="STRADIVARIUS",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="MANGO",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="PUBLIC",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="KOTSOVOLOS",
            category_name="Shopping"
        ),
        CategorizationRuleSeed(
            keyword="PLAISIO",
            category_name="Shopping"
        ),

        # -------------------------------------------------
        # Food & Coffee
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="OLYRA KALLIS",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="DRAKOPOULOS FRAGKISKOS",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="GRIGOBROS",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="OLYMPUS PLAZA",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="COFFEE ISLAND",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="ZACHAROPLASTEIO KOSMIK",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="CITY GRILL",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="ILIADIS COFFEE AND FOOD",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="MCDONALD",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="3K GELATO",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="SNAC BAR",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="PROMITHEAS ALEXANDRIS",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="EZEE ALMIROU",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="GOODYS",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="KFC",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="STARBUCKS",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="EVEREST",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="WOLT",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="EFOOD",
            category_name="Food & Coffee"
        ),
        CategorizationRuleSeed(
            keyword="BOX",
            category_name="Food & Coffee"
        ),

        # -------------------------------------------------
        # Health
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="FARMAKEIO",
            category_name="Health"
        ),
        CategorizationRuleSeed(
            keyword="PHARMACY",
            category_name="Health"
        ),
        CategorizationRuleSeed(
            keyword="KALLERGI",
            category_name="Health"
        ),
        CategorizationRuleSeed(
            keyword="STATHOPOULOU VLACH",
            category_name="Health"
        ),
        CategorizationRuleSeed(
            keyword="POULAKOS VASILIOS",
            category_name="Health"
        ),
        CategorizationRuleSeed(
            keyword="E PAPAKOSTA PHARMACY",
            category_name="Health"
        ),
        CategorizationRuleSeed(
            keyword="BIOIATRIKI",
            category_name="Health"
        ),
        CategorizationRuleSeed(
            keyword="IATROPOLIS",
            category_name="Health"
        ),
        CategorizationRuleSeed(
            keyword="OXINOIA",
            category_name="Health"
        ),
        CategorizationRuleSeed(
            keyword="ΙΑΤΡΟΣ",
            category_name="Health"
        ),
        CategorizationRuleSeed(
            keyword="DOCTOR",
            category_name="Health"
        ),

        # -------------------------------------------------
        # Transport
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="OASA",
            category_name="Transport"
        ),
        CategorizationRuleSeed(
            keyword="ATTIKI ODOS",
            category_name="Transport"
        ),
        CategorizationRuleSeed(
            keyword="NEA ODOS",
            category_name="Transport"
        ),
        CategorizationRuleSeed(
            keyword="EPASS.NAODOS.GR",
            category_name="Transport"
        ),
        CategorizationRuleSeed(
            keyword="DIODIA",
            category_name="Transport"
        ),
        CategorizationRuleSeed(
            keyword="FTP",
            category_name="Transport"
        ),
        CategorizationRuleSeed(
            keyword="AFTOKINITODROMOS KEN",
            category_name="Transport"
        ),
        CategorizationRuleSeed(
            keyword="TALIMA ELKA PARKING",
            category_name="Transport"
        ),
        CategorizationRuleSeed(
            keyword="UBER",
            category_name="Transport"
        ),
        CategorizationRuleSeed(
            keyword="FREE NOW",
            category_name="Transport"
        ),
        CategorizationRuleSeed(
            keyword="FREENOW",
            category_name="Transport"
        ),

        # -------------------------------------------------
        # Cash Withdrawal
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="ΑΝΑΛΗΨΗ ΑΠΟ ΑΤΜ",
            category_name="Cash Withdrawal"
        ),

        # -------------------------------------------------
        # Transfers
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="REVOLUT",
            category_name="Transfers"
        ),
        CategorizationRuleSeed(
            keyword="ΕΝΤΟΛΗ INSTANT TRANS",
            category_name="Transfers"
        ),
        CategorizationRuleSeed(
            keyword="IRIS",
            category_name="Transfers"
        ),

        # -------------------------------------------------
        # Loan Payments
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="LOAN",
            category_name="Loan Payments"
        ),
        CategorizationRuleSeed(
            keyword="ΔΟΣΗ ΔΑΝΕΙΟΥ",
            category_name="Loan Payments"
        ),

        # -------------------------------------------------
        # Insurance
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="ΖΗΤ5933",
            category_name="Insurance"
        ),
        CategorizationRuleSeed(
            keyword="BMI",
            category_name="Insurance"
        ),
        CategorizationRuleSeed(
            keyword="ΒΜΙ",
            category_name="Insurance"
        ),
        CategorizationRuleSeed(
            keyword="ΑΣΦΑΛΕΙΑ",
            category_name="Insurance"
        ),

        # -------------------------------------------------
        # Housing
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="KOINOHRIST",
            category_name="Housing"
        ),
        CategorizationRuleSeed(
            keyword="ΚΟΙΝΟΧΡΗΣΤ",
            category_name="Housing"
        ),
        CategorizationRuleSeed(
            keyword="ΣΚΥΡΟΥ 35",
            category_name="Housing"
        ),
        CategorizationRuleSeed(
            keyword="ΓΚΙΟΣΕΣ Λ ΝΟΕΜΒΡΗ 25",
            category_name="Housing"
        ),
        CategorizationRuleSeed(
            keyword="GKIOSES DECEMBER",
            category_name="Housing"
        ),
        CategorizationRuleSeed(
            keyword="ΓΚΙΟΣΕΣ ΜΑΙΟ 26",
            category_name="Housing"
        ),

        # -------------------------------------------------
        # Home & Household
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="PRAKTIKER",
            category_name="Home & Household"
        ),
        CategorizationRuleSeed(
            keyword="LEROY MERLIN",
            category_name="Home & Household"
        ),
        CategorizationRuleSeed(
            keyword="ERMIS 452",
            category_name="Home & Household"
        ),
        CategorizationRuleSeed(
            keyword="ERMIS 457",
            category_name="Home & Household"
        ),
        CategorizationRuleSeed(
            keyword="DIMTSIS GEORGIOS",
            category_name="Home & Household"
        ),
        CategorizationRuleSeed(
            keyword="KALAKOS STEFANOS",
            category_name="Home & Household"
        ),
        CategorizationRuleSeed(
            keyword="KTENAS P.GEORGE",
            category_name="Home & Household"
        ),
        CategorizationRuleSeed(
            keyword="IKEA",
            category_name="Home & Household"
        ),
        CategorizationRuleSeed(
            keyword="JYSK",
            category_name="Home & Household"
        ),

        # -------------------------------------------------
        # Car Maintenance
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="MAXX PARTS",
            category_name="Car Maintenance"
        ),
        CategorizationRuleSeed(
            keyword="SUPER CARWASH",
            category_name="Car Maintenance"
        ),

        # -------------------------------------------------
        # Bank Fees
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="ΕΞΟΔΑ ΕΝΤΟΛΗΣ",
            category_name="Bank Fees"
        ),
        CategorizationRuleSeed(
            keyword="ΕΞΟΔΑ INSTANT TRANSF",
            category_name="Bank Fees"
        ),

        # -------------------------------------------------
        # Taxes & Government
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="BEBAIOMENES",
            category_name="Taxes & Government"
        ),
        CategorizationRuleSeed(
            keyword="PARABOLO",
            category_name="Taxes & Government"
        ),

        # -------------------------------------------------
        # Travel
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="BOOKING.COM",
            category_name="Travel"
        ),
        CategorizationRuleSeed(
            keyword="AEGEAN",
            category_name="Travel"
        ),
        CategorizationRuleSeed(
            keyword="EKDROMI.GR",
            category_name="Travel"
        ),
        CategorizationRuleSeed(
            keyword="BLUE STAR",
            category_name="Travel"
        ),
        CategorizationRuleSeed(
            keyword="HOTEL ROTONDA",
            category_name="Travel"
        ),
        CategorizationRuleSeed(
            keyword="PORTO HELI HOTEL",
            category_name="Travel"
        ),
        CategorizationRuleSeed(
            keyword="GRAND HOTEL PALACE",
            category_name="Travel"
        ),
        CategorizationRuleSeed(
            keyword="TOURISMOS KAI DRASI",
            category_name="Travel"
        ),
        CategorizationRuleSeed(
            keyword="SKY EXPRESS",
            category_name="Travel"
        ),
        CategorizationRuleSeed(
            keyword="RYANAIR",
            category_name="Travel"
        ),
        CategorizationRuleSeed(
            keyword="AIRBNB",
            category_name="Travel"
        ),
        CategorizationRuleSeed(
            keyword="FERRYHOPPER",
            category_name="Travel"
        ),

        # -------------------------------------------------
        # Services
        # -------------------------------------------------

        CategorizationRuleSeed(
            keyword="PIPEROPOULOS MILTIADIS",
            category_name="Services"
        ),
    ],

    recurring_income_rules=[
        RecurringIncomeRuleSeed(
            name="Payroll",
            expected_amount=Decimal("2448.52"),
            expected_day=30,
            transaction_keyword="PAYROLL"
        ),

        RecurringIncomeRuleSeed(
            name="EFKA Pension",
            expected_amount=Decimal("393.81"),
            expected_day=24,
            transaction_keyword="ΣΥΝΤ.Ε.Φ.Κ.Α."
        ),
    ]
)