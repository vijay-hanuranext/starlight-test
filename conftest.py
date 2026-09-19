import os

import pytest
from dotenv import load_dotenv

from login_page import LoginPage

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