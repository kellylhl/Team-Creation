from playwright.sync_api import Page, expect


def test_registered_customer_can_log_in(page: Page) -> None:
    # sign in with a registered email
    email = f"tommy.l123@gmail.com"
    password = "Apex1234"

    # 1. Open the login page.
    page.goto("https://automationexercise.com/login")

    # Optional: close the cookie banner if the demo site displays it.
    consent_button = page.get_by_role("button", name="Consent")
    if consent_button.count() and consent_button.first.is_visible():
        consent_button.first.click()

    # 2. Enter the registered email address and password.
    # The first email field belongs to the Login form.
    page.locator("input[name='email']").first.fill(email)
    page.locator("input[name='password']").fill(password)

    # 3. Click the Login button.
    page.get_by_role("button", name="Login").click()

    # 4. Regression check: the website confirms the customer is logged in.
    expect(page.get_by_text("Logged in as")).to_be_visible()
