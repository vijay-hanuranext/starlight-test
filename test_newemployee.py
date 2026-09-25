from datetime import datetime

import pytest
from helpers import build_employee_data
from playwright.sync_api import Page, expect

from newemployee import EmployeesPage


def test_create_new_employee(logged_in_page: Page, employees_form_page):

    unique_id = datetime.now().strftime("%Y%m%d%H%M%S")
    full_name = f"John Smith{unique_id}"

    employee_form = employees_form_page
    employee_form.fill_employee(
        first_name="John",
        last_name=f"Smith{unique_id}",
        email=f"john.smith{unique_id}@gmail.com",
        title="QA Engineer",
        hire_date="2025-03-15",
    )
    employee_form.submit()
    expect(logged_in_page.get_by_text(full_name, exact=True)).to_be_visible(
        timeout=10000
    )

@pytest.mark.parametrize(
    "employee_data, missing_field",
    [
        (build_employee_data(first=""), "First name"),
        (build_employee_data(last=""), "Last name"),
        (build_employee_data(email=""), "Email"),
        (build_employee_data(title=""), "Title"),
        (build_employee_data(hire_date=""), "Hire date"),
    ],
)
def test_required_field_missing(employees_form_page, employee_data, missing_field):
    employees_form_page.fill_employee(
        employee_data["first"],
        employee_data["last"],
        employee_data["email"],
        employee_data["title"],
        employee_data["hire_date"],
    )
    employees_form_page.submit()
    expect(employees_form_page.error_banner).to_contain_text(
        f"Please fill in the required field: {missing_field}.",
        timeout=15000,
    )

def test_blankfields_submission(employees_form_page):
    employee_form = employees_form_page
    employee_form.submit()

    expect(
        employee_form.page.get_by_text(
            "Please fill in the required fields: First name, Last name, Email, Title, Hire date."
        )
    ).to_be_visible(timeout=10000)


def test_Invalidemail_formate(logged_in_page: Page, employees_form_page):
    employee_form = employees_form_page
    employee_form.fill_employee(
        first_name="Test",
        last_name="xyz",
        email="test@xyz",
        title="QA Engineer",
        hire_date="2025-01-20",
    )
    employee_form.submit()

    expect(
        logged_in_page.get_by_text("Please enter a valid email address")
    ).to_be_visible(timeout=10000)
