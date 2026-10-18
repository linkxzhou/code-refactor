"""Billing: pricing, invoice rendering and delivery (all in one place, for now)."""
import datetime
import json

TAX_RATES = {"DE": 0.19, "FR": 0.20, "US": 0.0}
MEMBER_DISCOUNT = 0.05


def smtp_send(to, subject, body):
    # Real implementation talks to the mail relay; tests patch billing.smtp_send.
    raise RuntimeError("SMTP not configured")


def line_total(item):
    total = item["price"] * item["qty"]
    if item["qty"] >= 10:
        total = total * 0.9
    return round(total, 2)


def compute_total(items, country, member=False):
    if country not in TAX_RATES:
        raise ValueError(f"unknown country: {country}")
    subtotal = sum(line_total(i) for i in items)
    if member:
        subtotal = subtotal * (1 - MEMBER_DISCOUNT)
    return round(subtotal * (1 + TAX_RATES[country]), 2)


def format_invoice(customer, items, country, member=False, today=None):
    today = today or datetime.date.today()
    lines = [f"INVOICE {customer['id']} {today.isoformat()}"]
    for i in items:
        lines.append(f"{i['sku']:<10}{i['qty']:>4} x {i['price']:>8.2f} = {line_total(i):>9.2f}")
    lines.append(f"TOTAL {compute_total(items, country, member):.2f}")
    return "\n".join(lines)


def invoice_json(customer, items, country, member=False):
    return json.dumps({
        "customer": customer["id"],
        "total": compute_total(items, country, member),
        "lines": [{"sku": i["sku"], "total": line_total(i)} for i in items],
    })


def send_invoice_email(customer, items, country, member=False):
    if not customer.get("email"):
        return False
    body = format_invoice(customer, items, country, member)
    smtp_send(customer["email"], f"Invoice {customer['id']}", body)
    return True
