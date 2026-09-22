from playwright.sync_api import Page


class LoginPage:
    def __init__(self, page):
        self.login_page = page

    def sign_in(self, username, password):
        self.login_page.get_by_role("textbox", name="Enter username or email").fill(username)
        self.login_page.get_by_test_id("login-password-input").fill(password)
        self.login_page.get_by_role("button", name="Sign in").click()    
