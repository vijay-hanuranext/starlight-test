from datetime import datetime

from faker import Faker

fake = Faker("en_AU")


def build_employee_data(
    first="Test",
    last="Gen",
    email=f"test.gen{datetime.now().strftime('%Y%m%d%H%M%S')}@gmail.com",
    title="Software Engineer",
    hire_date="2023-01-01",
):
    return {
        "first": first,
        "last": last,
        "email": email,
        "title": title,
        "hire_date": hire_date,
    }


def build_employee_payload():
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.unique.email(),
        "department": "engineering",
        "title": "Test Analyst",
        "hire_date": fake.date_between("-60d", "+30d").isoformat(),
    }
