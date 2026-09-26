import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page ,expect

from login_page import LoginPage
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
def sign_in_once(browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE_URL)
    login = LoginPage(page)
    login.sign_in(USERNAME, PWD)
    expect(page).to_have_url(f"{BASE_URL}/dashboard" , timeout=15000)
    context.close()
    