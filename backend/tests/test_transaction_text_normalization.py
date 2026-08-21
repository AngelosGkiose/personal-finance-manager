import pytest

from app.services.categorization_service import (
    normalize_transaction_text,
)


@pytest.mark.parametrize(
    "description, keyword",
    [
        (
            "SΚLΑVΕΝΙΤΙS_CΗΑLΑΝDRΙ",
            "SKLAVENITIS"
        ),
        (
            "ΑΒ_ΑG.ΡΑRΑSΚΕVΙ_1",
            "AB_"
        ),
        (
            "SΗΕLL ΜΥRΤΕΑ ΖΑΝ ΜΟRΕΑ",
            "SHELL"
        ),
        (
            "ΟLΥRΑ ΚΑLLΙS Ε Ε",
            "OLYRA KALLIS"
        ),
        (
            "S F G ΚΑLLΕRGΙ S SΚΟ",
            "KALLERGI"
        ),
        (
            "VΟDΑFΟΝΕ ΒΙLL ΡΑΥΜΕΝΤ",
            "VODAFONE"
        ),
        (
            "ΕΥDΑΡ ΒΙLL ΡΑΥΜΕΝΤ",
            "EYDAP"
        ),
        (
            "LΙDL",
            "LIDL"
        ),
        (
            "ΜΥ ΜΑRΚΕΤ 607 ΑG ΡΑRΑS",
            "MY MARKET"
        ),
        (
            "SΡΟΤΙFΥ Ρ4556Β9Β7F",
            "SPOTIFY"
        ),
        (
            "ΑΖΑRΙS ΕΕ",
            "AZARIS"
        ),
        (
            "RΕVΟLUΤ**0131*",
            "REVOLUT"
        ),
        (
            "ΡRΟΤΕRGΙΑ ΑΡΡ",
            "PROTERGIA"
        ),
        (
            "ΗΟΝDΟS CΕΝΤΕR",
            "HONDOS CENTER"
        ),
        (
            "ΤSΑΚΙRΙS-ΜΑLLΑS_CΗΑLΑΝ",
            "TSAKIRIS"
        ),
        (
            "ΟΑSΑ ΕΤΙCΚΕΤ ΡΟS",
            "OASA"
        ),
        (
            "IRIS-ΕΥΔΑΠ ΑΕ",
            "EYDAP"
        ),
        (
            "ΙRΙS 6938973337",
            "IRIS"
        ),
        (
            "ΡRΑΚΤΙΚΕR ΜΑΝDRΑ ΑΤΤΙΚ",
            "PRAKTIKER"
        ),
        (
            "ΝΑVΥ ΑΝD GRΕΕΝ ΜCΑRΤΗU",
            "NAVY AND GREEN"
        ),
        (
            "GRΙGΟΒRΟS Ο.Ε.",
            "GRIGOBROS"
        ),
        (
            "ΝΙΚΕ RΕΤΑΙL",
            "NIKE"
        ),
        (
            "SΑLΑRΥ JUΝΕ 2026",
            "SALARY"
        ),
        (
            "ΡΑΥRΟLL 07.2026",
            "PAYROLL"
        ),
    ]
)
def test_normalized_description_contains_expected_keyword(
    description,
    keyword
):
    normalized_description = normalize_transaction_text(
        description
    )

    normalized_keyword = normalize_transaction_text(
        keyword
    )

    assert normalized_keyword in normalized_description

def test_normalize_transaction_text_removes_extra_spaces():
    result = normalize_transaction_text(
        "  VODAFONE    BILL   "
    )

    assert result == "VODAFONE BILL"


def test_normalize_transaction_text_converts_to_uppercase():
    result = normalize_transaction_text(
        "netflix"
    )

    assert result == "NETFLIX"


def test_normalize_transaction_text_keeps_numbers_and_symbols():
    result = normalize_transaction_text(
        "RΕVΟLUΤ**0131*"
    )

    assert result == "REVOLUT**0131*"