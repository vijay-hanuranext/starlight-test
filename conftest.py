import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page

from login_page import LoginPage
from newemployee import EmployeesPage
from registeruser import RegisterPage

load_dotenv()

BASE_URL = os.environ["BASE_URL"]
USERNAME = os.getenv("CRM_USERNAME")
PWD = os.getenv("CRM_PASSWORD")


@pytest.fixture
def logged_in_page(page):
    page.goto(BASE_URL)
    login = LoginPage(page)
    login.sign_in(USERNAME, PWD)
    return page


@pytest.fixture
def register_page(page: Page):
    page.goto("https://crm.hanuranext.com/login")
    register_page = RegisterPage(page)
    register_page.go_to_registration()
    return register_page


@pytest.fixture
def employees_form_page(logged_in_page):
    employees_page = EmployeesPage(logged_in_page)
    return employees_page.open_new_employee_form()
