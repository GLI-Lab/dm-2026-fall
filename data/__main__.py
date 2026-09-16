"""python -m data — verify that every course dataset loads."""

from data.loader import check_datasets

table = check_datasets()
print(table.to_string(index=False))
if (table["status"] != "ok").any():
    raise SystemExit(1)
