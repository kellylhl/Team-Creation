import re

from playwright.sync_api import Page, expect


def open_products_page(page: Page) -> None:
    # Open Products page and close the cookie consent when appears
    page.goto("https://automationexercise.com/products")

    consent_button = page.get_by_role("button", name="Consent")
    if consent_button.count() and consent_button.first.is_visible():
        consent_button.first.click()


def test_find_products_by_category(page: Page) -> None:
    # 1. Open the products page.
    open_products_page(page)

    # 2. Expand the Women category and choose Tops.
    page.locator("a[href='#Women']").click()
    page.locator("a[href='/category_products/2']").click()

    # 3. Verify the products displayed match with the category filter
    expect(page.get_by_text(re.compile("Women - Tops Products", re.I))).to_be_visible()


def test_find_products_by_brand(page: Page) -> None:
    # 1. Open the products page.
    open_products_page(page)

    # 2. Select the Polo brand filter.
    page.locator("a[href='/brand_products/Polo']").click()

    # 3. Verify the products displayed match the brand filter
    expect(page.get_by_text(re.compile("Brand - Polo Products", re.I))).to_be_visible()


def test_find_products_by_keyword_search(page: Page) -> None:
    # 1. Open the products page.
    open_products_page(page)

    # 2. Enter a product keyword and click Search.
    page.locator("#search_product").fill("Blue Top")
    page.locator("#submit_search").click()

    # 3. Verify the products being filtered are contextual
    expect(page.get_by_text("SEARCHED PRODUCTS")).to_be_visible()
    expect(page.get_by_text("Blue Top").first).to_be_visible()
    
