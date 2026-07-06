def clean_order_items(rows):
    result = []

    for r in rows:
        if r["product_id"] == "P999":
            continue

        r["quantity"] = int(r["quantity"])
        r["unit_price"] = float(r["unit_price"])
        r["discount"] = float(r["discount"] or 0)

        result.append(r)

    return result