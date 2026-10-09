from playwright.sync_api import expect

def test_employee_profile(logged_in_page, api_employee):
    logged_in_page.goto(f"/employees/{api_employee['id']}")
    name = f"{api_employee['first_name']} {api_employee['last_name']}"
    expect(logged_in_page.get_by_text(name).first).to_be_visible()
