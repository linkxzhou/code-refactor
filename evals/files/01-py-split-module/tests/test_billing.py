import datetime
from unittest import mock

import billing

ITEMS = [{"sku": "A1", "price": 9.99, "qty": 3}, {"sku": "B2", "price": 1.5, "qty": 12}]


def test_total_de_member():
    assert billing.compute_total(ITEMS, "DE", member=True) == 52.2


def test_unknown_country():
    try:
        billing.compute_total(ITEMS, "XX")
    except ValueError as e:
        assert str(e) == "unknown country: XX"
    else:
        raise AssertionError("expected ValueError")


def test_invoice_text():
    text = billing.format_invoice({"id": "C7"}, ITEMS, "US", today=datetime.date(2026, 1, 2))
    assert text.splitlines()[0] == "INVOICE C7 2026-01-02"
    assert text.splitlines()[-1] == "TOTAL 46.17"


def test_email_uses_smtp():
    with mock.patch("billing.smtp_send") as send:
        assert billing.send_invoice_email({"id": "C7", "email": "a@b.c"}, ITEMS, "FR") is True
    send.assert_called_once()


def test_no_email():
    assert billing.send_invoice_email({"id": "C7"}, ITEMS, "FR") is False
