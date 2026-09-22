import os
import random
from playwright.sync_api import expect
from login_page import LoginPage
from dotenv import load_dotenv

load_dotenv()

Base_url = os.environ["BASE_URL"]
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

def test_login(logged_in_page):

    expect(logged_in_page).to_have_url("https://crm.hanuranext.com/login" , timeout=15000)
    logged_in_page.get_by_role("link", name="Employees").click()
    expect(logged_in_page).to_have_url("https://crm.hanuranext.com/employees")
    logged_in_page.get_by_role("link", name="+ New employee").click()
    expect(logged_in_page).to_have_url("https://crm.hanuranext.com/employees/new")
    number = random.randint(1, 10000)
    logged_in_page.get_by_role("textbox", name="FIRST NAME").fill("John")
    logged_in_page.get_by_role("textbox", name="LAST NAME").fill(f"Smith{number}")
    # get email using test_id
    logged_in_page.get_by_test_id("employee-form-email").fill(f"johnsmith{number}@abc.com")
    logged_in_page.get_by_test_id("employee-form-title").fill("Software Engineer")
    # get department using combobox and fill qa
    logged_in_page.get_by_test_id("employee-form-department").select_option("QA")
    # populate hire date using role and name
    logged_in_page.get_by_role("textbox", name="HIRE DATE").fill("2023-06-01")
    logged_in_page.get_by_role("button", name="Create employee").click(timeout=15000)
    logged_in_page.pause()


    logged_in_page.get_by_role("link", name="Back to employees").click()
    expect(logged_in_page).to_have_url("https://crm.hanuranext.com/employees")
    logged_in_page.pause()


    logged_in_page.goto("https://crm.hanuranext.com/employees")
    logged_in_page.get_by_placeholder("Search by name, title, or email...").fill(f"John Smith{number}")
    
    logged_in_page.pause()

