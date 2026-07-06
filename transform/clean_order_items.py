def clean_order_items(rows):
    result = []
    seen = set()
    for r in rows:
        r = r.copy() #tao ban sao cua dictionary
        if r["product_id"] == "P999":
            continue
        a = r["order_id"]
        if a in seen: #duplicate
            continue
        seen.add(a)
        r["quantity"] = int(r["quantity"])
        r["unit_price"] = float(r["unit_price"])
        r["discount"] = float(r["discount"] or 0)

        result.append(r)

    return result