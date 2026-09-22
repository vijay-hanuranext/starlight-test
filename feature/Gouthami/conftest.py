import os
import pytest
from dotenv import load_dotenv
from login_page import LoginPage

load_dotenv()

BASE_URL = os.environ["BASE_URL"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

@pytest.fixture
def logged_in_page(page):
    page.goto(BASE_URL)
    LoginPage(page).sign_in(USERNAME, PASSWORD)
    return page


