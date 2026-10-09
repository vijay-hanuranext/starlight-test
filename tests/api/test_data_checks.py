from datetime import date
import time

import pytest
import sqlite_utils
from utils.snapshot import take_snapshot

@pytest.fixture
def db(api, tmp_path):
    path = str(tmp_path / "snapshot.db")
    take_snapshot(api, path)
    return sqlite_utils.Database(path)

def test_headcount_matches_dashboard(api, db):
    rows = db.query(
        "SELECT department, COUNT(*) AS n FROM employees GROUP BY department"
    )
    counts = {row["department"]: row["n"] for row in rows}
    summary = api.get("/dashboard/summary").json()
    expected = summary["headcount_by_department"]
    assert counts == expected

def test_no_manager_points_at_nobody(db):
    orphans = db.execute(
        "SELECT COUNT(*) FROM employees e "
        "LEFT JOIN employees m ON e.manager_id = m.id "
        "WHERE e.manager_id IS NOT NULL AND m.id IS NULL"
    ).fetchone()[0]
    assert orphans == 0

def person(email):
    return {
        "first_name": "Jane", "last_name": "Citizen",
        "email": email, "department": "engineering",
        "title": "Test Analyst",
        "hire_date": date.today().isoformat(),
    }

def test_no_duplicate_emails_ignoring_case(api, tmp_path):
    email = f"jane.{time.time_ns()}@example.com"
    created = []
    try:
        for e in (email, email.upper()):
            created.append(api.post("/employees", json=person(e)))
        path = str(tmp_path / "dup.db")
        take_snapshot(api, path)
        sql = "SELECT lower(email) FROM employees GROUP BY lower(email) HAVING COUNT(*) > 1"
        dupes = sqlite_utils.Database(path).execute(sql).fetchall()
        assert dupes == []
    finally:
        for r in created:
            if r.status_code == 201:
                api.delete(f"/employees/{r.json()['id']}")

def test_every_employee_was_copied(api, db):
    from_api = api.get("/employees").json()
    assert db["employees"].count == len(from_api)

def test_postcodes_are_four_characters(db):
    bad = db.execute(
        "SELECT postcode FROM employees "
        "WHERE postcode IS NOT NULL AND length(postcode) != 4"
    ).fetchall()
    assert bad == []

def test_required_fields_are_filled(db):
    missing = db.execute(
        "SELECT id FROM employees WHERE first_name IS NULL "
        "OR last_name IS NULL OR email IS NULL "
        "OR department IS NULL OR title IS NULL "
        "OR hire_date IS NULL"
    ).fetchall()
    assert missing == []
