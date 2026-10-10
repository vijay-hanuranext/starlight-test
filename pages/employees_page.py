
from playwright.sync_api import Page

from pages.employee_form_page import EmployeeFormPage


class EmployeesPage:
    def __init__(self, page: Page):
        self.page = page
        self.employees_link = page.get_by_role("link", name="Employees")
        self.new_employee_link = page.get_by_role("link", name="+ New employee")

    def go_to_employees(self):
        self.employees_link.click()

    def click_new_employee(self):
        self.new_employee_link.click()

    def open_new_employee_form(self):
        self.go_to_employees()
        self.click_new_employee()
        return EmployeeFormPage(self.page)
