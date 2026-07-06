def clean_sellers(rows):

    cleaned = []
    seen = set()
    city_map = {
        "hanoi": "Hanoi",
        "ha noi": "Hanoi",
        "hcm": "Ho Chi Minh",
        "ho chi minh": "Ho Chi Minh",
        "da nang": "Da Nang",
        "hai phong": "Hai Phong"
    }
    for row in rows:
        r = row.copy() #tao ban sao cua dictionary
        seller_id = row["seller_id"].strip()
        # seller_id rỗng
        if not seller_id:
            continue

        # duplicate
        if seller_id in seen:
            continue
        seen.add(seller_id)

        # seller_name rỗng
        if not row["seller_name"].strip():
            continue
        # chuẩn hóa tên
        row["seller_name"] = (
            row["seller_name"]
            .strip()
            .title()
        )
        # chuẩn hóa city
        city = (
            row["city"]
            .strip()
            .lower()
        )
        row["city"] = city_map.get(
            city,
            "Unknown"
        )
        cleaned.append(row)
    return cleaned