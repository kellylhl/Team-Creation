from playwright.sync_api import Page, expect


def test_complete_an_order(page: Page) -> None:
    email = f"tommy.l123@gmail.com"
    password = "Apex1234"

    # 1. Log in.
    page.goto("https://automationexercise.com/login")

    consent_button = page.get_by_role("button", name="Consent")
    if consent_button.count() and consent_button.first.is_visible():
        consent_button.first.click()

    page.locator("input[name='email']").first.fill(email)
    page.locator("input[name='password']").fill(password)
    page.get_by_role("button", name="Login").click()
    expect(page.get_by_text("Logged in as Tommy")).to_be_visible()

    # 2. Open Products, move over Blue Top, then add it to the cart.
    page.goto("https://automationexercise.com/products")
    blue_top = page.locator(".product-image-wrapper").filter(has_text="Blue Top").first
    blue_top.hover()
    blue_top.locator(".overlay-content .add-to-cart").click()
    expect(page.get_by_text("Added!")).to_be_visible()

    # 3. Click View Cart on the prompt to go to the cart page.
    page.get_by_role("link", name="View Cart").click()

    # 4. Check both items and their quantity, then begin checkout.
    expect(page.get_by_text("Blue Top", exact=True)).to_be_visible()
    page.get_by_text("Proceed To Checkout", exact=True).click()

    # 5. Verify delivery and billing address details.
    delivery_address = page.locator("#address_delivery")
    billing_address = page.locator("#address_invoice")
    expect(delivery_address).to_contain_text("Tommy Lee")
    expect(delivery_address).to_contain_text("123 gardens")
    expect(billing_address).to_contain_text("Tommy Lee")
    expect(billing_address).to_contain_text("123 gardens")

    # 6. Review the order, scroll to Place Order, and click it.
    expect(page.get_by_text("Review Your Order")).to_be_visible()
    place_order = page.get_by_text("Place Order", exact=True)
    place_order.scroll_into_view_if_needed()
    place_order.click()

    # 7. Enter demo card details.
    page.locator("input[name='name_on_card']").fill("Tommy Lee")
    page.locator("input[name='card_number']").fill("4423456765432878")
    page.locator("input[name='cvc']").fill("123")
    page.locator("input[name='expiry_month']").fill("08")
    page.locator("input[name='expiry_year']").fill("2029")

    # 8. Pay and confirm the order, then check the success message.
    page.get_by_role("button", name="Pay and Confirm Order").click()
    expect(page.get_by_text("ORDER PLACED!")).to_be_visible()
