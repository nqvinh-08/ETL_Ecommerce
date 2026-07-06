def clean_products(rows):
    seen = set()
    result = []

    for r in rows:
        r = r.copy() #tao ban sao cua dictionary
        
        pid = r["product_id"]
        if pid in seen: #duplicate
            continue
        seen.add(pid)

        r["category"] = r["category"].title()
        r["brand"] = r["brand"].title()

        result.append(r)

    return result