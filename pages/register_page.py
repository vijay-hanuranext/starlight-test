from playwright.sync_api import Page


class RegisterPage:

  def __init__(self, page: Page):
      self.page = page
      self.account_link = page.get_by_role("link", name ="Register an account")


    
      self.create_account_heading = page.get_by_role("heading", name="Create account")
      self.full_name_input = page.get_by_test_id("register-fullname-input")
      self.username_input = page.get_by_test_id("register-username-input")
      self.email_input = page.get_by_test_id("register-email-input")
      self.password_input = page.get_by_test_id("register-password-input")
      self.submit_button = page.get_by_test_id("register-submit-button")


  def go_to_registration(self):
      self.account_link.click()

  def fill_registration(self, full_name, username, email, password):
      self.full_name_input.fill(full_name)
      self.username_input.fill(username)
      self.email_input.fill(email)
      self.password_input.fill(password)

  def submit(self):
    self.submit_button.click()



