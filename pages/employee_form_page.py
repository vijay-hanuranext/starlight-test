from playwright.sync_api import Page


class EmployeeFormPage:
    def __init__(self, page: Page):
        self.page = page
        self.first_name_input = page.get_by_label("First Name")
        self.last_name_input = page.get_by_label("Last Name")
        self.email_input = page.get_by_test_id("employee-form-email")
        self.title_input = page.get_by_test_id("employee-form-title")
        self.hire_date_input = page.get_by_test_id("employee-form-hire-date")
        self.submit_button = page.get_by_test_id("employee-form-submit")

    @property
    def error_banner(self):
        return self.page.get_by_test_id("employee-form-error-banner")

    @property
    def address_line1(self):
        return self.page.get_by_role("combobox", name="Address Line 1")

    def fill_employee(self, first_name, last_name, email, title, hire_date):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.title_input.fill(title)
        self.hire_date_input.fill(hire_date)

    def submit(self):
        self.submit_button.click()
