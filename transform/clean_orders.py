from datetime import datetime


def parse_date(date_str):
    if not date_str:
        return None

    date_str = date_str.replace("/", "-") #thay / --> -

    for fmt in ("%Y-%m-%d", "%d-%m-%Y"):
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    raise ValueError(f"Invalid date format: {date_str}")


def clean_orders(rows):
    seen = set()
    result = []

    for r in rows:
        r = r.copy() #tao bản sao của dictionary
        r.pop("seller_id", None) #neu ko co tra ve none
        order_id = r["order_id"]
        if order_id in seen : #duplicate
            continue
        seen.add(order_id)
        if not r["order_date"]:
            continue
        r["order_date"] = parse_date(r["order_date"])
        r["ship_date"] = parse_date(r["ship_date"])

        result.append(r)

    return result