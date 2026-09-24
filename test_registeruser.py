import random
import re

from playwright.sync_api import expect


def test_register_happy_path(register_page):
    unique_id = random.randint(100, 999)
    register_page.fill_registration(
        full_name=f"Test Abc{unique_id}",
        username=f"testabc{unique_id}",
        email=f"testabc{unique_id}@gmail.com",
        password="Test@1234",
    )
    register_page.submit()
    expect(register_page.page.get_by_text("Good morning")).to_be_visible(timeout=30000)


def test_register_duplicate_username(register_page):
    unique_id = random.randint(100, 999)
    register_page.fill_registration(
        full_name=f"Test Abc{unique_id}",
        username="Test_abc",
        email=f"newemail{unique_id}@gmail.com",
        password="Test@1234",
    )
    register_page.submit()
    expect(register_page.page.get_by_text("Username already taken")).to_be_visible(
        timeout=10000
    )


def test_register_duplicate_email(register_page):
    unique_id = random.randint(100, 999)
    register_page.fill_registration(
        full_name=f"Test Abc{unique_id}",
        username=f"newuser{unique_id}",
        email="test.abc@gmail.com",
        password="Test@1234",
    )
    register_page.submit()
    expect(register_page.page.get_by_text("Email already registered")).to_be_visible(
        timeout=10000
    )


def test_password_rules_validation(register_page):
    page = register_page.page
    register_page.password_input.fill("abc")

    uppercase_rule = page.locator(
        '[data-testid="password-rules"] li', has_text="One uppercase letter"
    )
    expect(uppercase_rule).to_have_class(re.compile("text-crm-muted"))
    expect(register_page.submit_button).to_be_disabled()

    register_page.password_input.fill("Abc12345!")

    uppercase_rule = page.locator(
        '[data-testid="password-rules"] li', has_text="One uppercase letter"
    )
    special_char_rule = page.locator(
        '[data-testid="password-rules"] li', has_text="One special character"
    )

    expect(uppercase_rule).to_have_class(re.compile("text-crm-success"))
    expect(special_char_rule).to_have_class(re.compile("text-crm-success"))
    expect(register_page.submit_button).to_be_enabled()
