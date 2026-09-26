def test_login_page_looks_right(page, base_url, assert_snapshot):
    page.goto(base_url)
    assert_snapshot(page.screenshot())