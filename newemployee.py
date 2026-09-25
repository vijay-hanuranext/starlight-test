from playwright.sync_api import Page


class EmployeesPage:
    def __init__(self, page: Page):
        self.page = page
        self.employees_link = page.get_by_role("link", name="Employees")
        self.new_employee_link = page.get_by_role("link", name="+ New employee")

    def go_to_employees(self):
        self.employees_link.click()

    def click_new_employee(self):
        self.new_employee_link.click()


class EmployeeFormPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.get_by_label("First Name")
        self.last_name_input = page.get_by_label("Last Name")
        self.email_input = page.get_by_test_id("employee-form-email")
        self.title_input = page.get_by_test_id("employee-form-title")
        self.hire_date_input = page.get_by_test_id("employee-form-hire-date")
        self.submit_button = page.get_by_test_id("employee-form-submit")

    def fill_employee(self, first_name, last_name, email, title, hire_date):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.title_input.fill(title)
        self.hire_date_input.fill(hire_date)

    def submit(self):
        self.submit_button.click()
