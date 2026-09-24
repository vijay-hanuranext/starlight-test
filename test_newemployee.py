from datetime import datetime

from playwright.sync_api import Page, expect

from newemployee import EmployeeFormPage, EmployeesPage


def test_create_new_employee(logged_in_page: Page):

    unique_id = datetime.now().strftime("%Y%m%d%H%M%S")
    full_name = f"John Smith{unique_id}"

    employees_page = EmployeesPage(logged_in_page)
    employees_page.go_to_employees()
    employees_page.click_new_employee()

    employee_form = EmployeeFormPage(logged_in_page)
    employee_form.fill_employee(
        first_name="John",
        last_name=f"Smith{unique_id}",
        email=f"john.smith{unique_id}@gmail.com",
        title="QA Engineer",
        hire_date="2025-03-15"
    )
    employee_form.submit()
    expect(logged_in_page.get_by_text(full_name, exact=True)).to_be_visible(timeout=10000)

def test_blankfields_submission(logged_in_page: Page):
    employees_page = EmployeesPage(logged_in_page)
    employees_page.go_to_employees()
    employees_page.click_new_employee()

    employee_form = EmployeeFormPage(logged_in_page)
    employee_form.submit()

    expect(logged_in_page.get_by_text("Please fill in the required fields: First name, Last name, Email, Title, Hire date.")).to_be_visible(timeout=10000)

def test_Invalidemail_formate(logged_in_page: Page):

    employees_page = EmployeesPage(logged_in_page)
    employees_page.go_to_employees()
    employees_page.click_new_employee()

    employee_form = EmployeeFormPage(logged_in_page)
    employee_form.fill_employee(
        first_name="Test",
        last_name="xyz",
        email="test@xyz",
        title="QA Engineer",
        hire_date="2025-01-20"
    )
    employee_form.submit()

    expect(logged_in_page.get_by_text("Please enter a valid email address")).to_be_visible(timeout=10000)


