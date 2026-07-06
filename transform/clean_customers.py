def clean_customers(rows):
    gender_map = {
        "m": "Male", "male": "Male",
        "f": "Female", "female": "Female",
        "nam": "Male", "nu": "Female", "nữ": "Female"
    }

    city_map = {
        "hanoi": "Hanoi",
        "ha noi": "Hanoi",
        "hcm": "Ho Chi Minh",
        "ho chi minh": "Ho Chi Minh",
        "da nang": "Da Nang",
        "hai phong": "Hai Phong"
    }

    seen = set()
    result = []

    for r in rows:
        cid = r["customer_id"]

        if cid in seen:
            continue
        seen.add(cid)
        r["customer_name"] = r["customer_name"].strip().title() #xoa khoang trang dauu cuoi
        r["gender"] = gender_map.get(r["gender"].strip().lower(), "Unknown")
        r["city"] = city_map.get(r["city"].strip().lower(), r["city"].strip().title())
        r["segment"] = (r["segment"] or "Regular").title()

        result.append(r)

    return result