from billing import TAX_RATES, compute_total, format_invoice, invoice_json, send_invoice_email


def checkout(customer, items, country):
    if country not in TAX_RATES:
        return {"error": "unsupported country"}
    total = compute_total(items, country, member=customer.get("member", False))
    send_invoice_email(customer, items, country, member=customer.get("member", False))
    return {"total": total, "invoice": format_invoice(customer, items, country), "json": invoice_json(customer, items, country)}
