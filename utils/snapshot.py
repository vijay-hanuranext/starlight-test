import sqlite_utils

KEEP = [
    "id", "first_name", "last_name", "email", "department",
    "title", "hire_date", "manager_id", "postcode",
]

def take_snapshot(api, path):
    rows = api.get("/employees").json()
    rows = [{k: row[k] for k in KEEP} for row in rows]
    db = sqlite_utils.Database(path)
    db["employees"].insert_all(rows, pk="id", replace=True)
