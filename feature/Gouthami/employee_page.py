from playwright.sync_api import Page


class EmployeePage:
    def __init__(self, page):
        self.employee_page = page

    def new_employee_form(self):
        self.employee_page.get_by_role("link", name="Employees").click()    