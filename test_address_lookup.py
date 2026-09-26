from playwright.sync_api import expect

from newemployee import EmployeeFormPage


def test_address_lookup_returns_the_mocked_suggestions(employees_form_page : EmployeeFormPage):
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