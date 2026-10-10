import re

from playwright.sync_api import Page, expect

from conftest import BASE_URL, PWD, USERNAME
from pages.login_page import LoginPage


def test_login_succeeds(page):
    page.goto(BASE_URL)
    login = LoginPage(page)
    login.sign_in(USERNAME, PWD)
    expect(
        page.get_by_text(re.compile(r"Good (morning|afternoon|evening)"))
    ).to_be_visible(timeout=15000)
    expect(page).to_have_url(f"{BASE_URL}/dashboard")


def test_invalid_user(page):
    page.goto(BASE_URL)
    login = LoginPage(page)
    login.sign_in("WRONGUSERNAME", PWD)
    expect(page.get_by_test_id("login-error-banner")).to_be_visible(timeout=15000)


def test_invalid_password(page):
    page.goto(BASE_URL)
    login = LoginPage(page)
    login.sign_in(USERNAME, "WRONGPASSWORD")
    expect(page.get_by_test_id("login-error-banner")).to_be_visible(timeout=15000)


def test_blank_signin_blocked_by_native_validation(page: Page):
    page.goto(BASE_URL)
    page.get_by_test_id("login-submit-button").click()
    expect(page).to_have_url(f"{BASE_URL}/login")
    expect(page.get_by_test_id("login-identifier-input")).to_have_js_property(
        "validity.valid", False
    )
