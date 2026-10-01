from datetime import datetime


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
