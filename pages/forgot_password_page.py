from playwright.sync_api import Page


class ForgotpasswordPage:
    def __init__(self, page: Page):
        self.page = page
        self.forgot_password_link = page.get_by_text("Forgot password?")
        self.email_input = page.get_by_placeholder("you@example.com")        
        self.send_reset_link = page.get_by_role("button", name="Send reset link")
        self.check_inbox_heading = page.get_by_role("heading", name="Check your inbox")
        self.expiry_text = page.get_by_text("expires in 1 hour")
        self.back_to_sign_in_link = page.get_by_role("link", name="Back to sign in")

    def go_to_forgotpassword(self):
        self.forgot_password_link.click()
        self.email_input.wait_for()

    def enter_email(self, email: str):
        self.email_input.fill(email)

    def click_send_reset_link(self):
        self.send_reset_link.click()

    def click_back_to_sign_in_link(self):
        self.back_to_sign_in_link.click()