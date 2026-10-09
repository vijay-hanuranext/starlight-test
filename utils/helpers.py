import uuid
from datetime import datetime

from faker import Faker

fake = Faker("en_AU")


def unique_suffix():
    """<yymmdd>_<6 char hex>, e.g. 261010_a3f9c1"""
    return f"{datetime.now().strftime('%y%m%d')}_{uuid.uuid4().hex[:6]}"


def build_employee_data(
    first="Test",
    last=None,
    email=None,
    title="Software Engineer",
    hire_date="2023-01-01",
):
    suffix = unique_suffix()
    return {
        "first": first,
        "last": f"Gen{suffix}" if last is None else last,
        "email": f"test.gen{suffix}@gmail.com" if email is None else email,
        "title": title,
        "hire_date": hire_date,
    }


def build_employee_payload():
    suffix = unique_suffix()
    first = fake.first_name()
    return {
        "first_name": first,
        "last_name": f"{fake.last_name()}{suffix}",
        "email": f"{first.lower()}.{suffix}@example.com",
        "department": "engineering",
        "title": "Test Analyst",
        "hire_date": fake.date_between("-60d", "+30d").isoformat(),
    }
