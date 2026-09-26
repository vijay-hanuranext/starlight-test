from playwright.sync_api import expect

from conftest import BASE_URL


def count_and_continue(calls):
    def handler(route):
        calls.append(route.request.url)
        route.continue_()
    return handler

def test_search_fires_the_api_once_per_pause(logged_in_page, base_url):
    logged_in_page.goto(f"{BASE_URL}/employees")
    total_count = logged_in_page.get_by_test_id("employees-total-count")
    expect(total_count).not_to_have_text("0 people across the company")

    calls = []
    logged_in_page.route("**/api/employees*", count_and_continue(calls))
    logged_in_page.get_by_test_id("employees-search-input").type("zzz-nobody-matches-this", delay=30)
    expect(total_count).to_have_text("0 people across the company")

    assert len(calls) == 1