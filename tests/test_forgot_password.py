import re
from playwright.sync_api import expect

RESET_EMAIL = "mohsinatestreset@gmail.com"
UNREGISTERED_EMAIL = "no.account.here@example.com"


def test_request_reset_link_with_registered_email(forgotpassword_page):
    forgotpassword_page.enter_email(RESET_EMAIL)
    forgotpassword_page.click_send_reset_link()

    expect(forgotpassword_page.check_inbox_heading).to_be_visible(timeout=30000)
    expect(forgotpassword_page.expiry_text).to_be_visible()

def test_request_reset_link_with_unregistered_email(forgotpassword_page):
    forgotpassword_page.enter_email(UNREGISTERED_EMAIL)
    forgotpassword_page.click_send_reset_link()

    expect(forgotpassword_page.check_inbox_heading).to_be_visible(timeout=30000)
    expect(forgotpassword_page.expiry_text).to_be_visible()

def test_back_to_sign_in(forgotpassword_page, base_url):
    forgotpassword_page.enter_email(RESET_EMAIL)
    forgotpassword_page.click_send_reset_link()

    expect(forgotpassword_page.check_inbox_heading).to_be_visible(timeout=30000)
    forgotpassword_page.click_back_to_sign_in_link()
    expect(forgotpassword_page.page).to_have_url(f"{base_url}/login")
