from playwright.sync_api import expect

from pages.employees_page import EmployeesPage


def test_address_lookup_returns_the_mocked_suggestions(employees_form_page: EmployeesPage):
    page = employees_form_page.page
    fake_suggestions = [
        {"place_id": "fake-1", "description": "1 Main Street, Sydney NSW 2000"},
        {"place_id": "fake-2", "description": "1 Main Street, Perth WA 6000"},
    ]

    def fulfill_with_fake_suggestions(route):
        route.fulfill(json=fake_suggestions)

    page.route(
        "**/api/geo/address-autocomplete*",
        fulfill_with_fake_suggestions,
    )
    employees_form_page.address_line1.fill("1 Main")
    options = page.get_by_role("listbox", name="Address suggestions").get_by_role("option")
    expect(options).to_have_count(2)

def test_a_failed_lookup_shows_no_suggestions(employees_form_page):
    page = employees_form_page.page

    def fail_with_service_error(route):
        route.fulfill(status=503, json={"detail": "not configured"})

    page.route(
        "**/api/geo/address-autocomplete*",
        fail_with_service_error,
    )

    employees_form_page.address_line1.fill("1 Main")
    expect(page.locator("#address-suggestions")).to_have_count(0)  
    #employees_form_page.page.pause()  # Pause to allow time to see the failed lookup in the UI