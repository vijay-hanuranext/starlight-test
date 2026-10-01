import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

from pages.employees_page import EmployeesPage
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

STORAGE_STATE_PATH = Path(".auth/state.json")
load_dotenv()

BASE_URL = os.environ["BASE_URL"]
USERNAME = os.getenv("CRM_USERNAME")
PWD = os.getenv("CRM_PASSWORD")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def logged_in_page(page):
    page.goto(BASE_URL)
    # login = LoginPage(page)
    # login.sign_in(USERNAME, PWD)
    return page


@pytest.fixture(scope="session")
def storage_state(browser):
    if not STORAGE_STATE_PATH.exists() or not session_is_valid(browser):
        STORAGE_STATE_PATH.parent.mkdir(exist_ok=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(BASE_URL)
        LoginPage(page).sign_in(USERNAME, PWD)
        expect(page).to_have_url(f"{BASE_URL}/dashboard", timeout=15000)
        context.storage_state(path=STORAGE_STATE_PATH)
        context.close()
    return str(STORAGE_STATE_PATH)


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


@pytest.fixture
def sign_in_once(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE_URL)
    login = LoginPage(page)
    login.sign_in(USERNAME, PWD)
    expect(page).to_have_url(BASE_URL + "/dashboard", timeout=15000)
    context.close()


def session_is_valid(browser):
    context = browser.new_context(storage_state=STORAGE_STATE_PATH)
    page = context.new_page()
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_load_state("networkidle")
    is_valid = "/login" not in page.url
    context.close()
    return is_valid


@pytest.fixture
def browser_context_args(browser_context_args, request, storage_state):
    if "logged_in_page" in request.fixturenames:
        return {**browser_context_args, "storage_state": storage_state}
    else:
        return browser_context_args
