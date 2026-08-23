from uuid import uuid4

from playwright.sync_api import Page, expect


def test_customer_can_sign_up(page: Page) -> None:
    # Create a different email address each time the test runs.
    unique_id = uuid4().hex[:8]
    name = "Tommy Lee"
    email = f"tommy.{unique_id}@gmail.com"
    password = "Apex1234"

    # 1. Open the sign-up page.
    page.goto("https://automationexercise.com/login")

    # to remove the consent prompt
    consent_button = page.get_by_role("button", name="Consent")
    if consent_button.count() and consent_button.first.is_visible():
        consent_button.first.click()

    # 2. Fill in the short sign-up form.
    page.get_by_placeholder("Name").fill(name)
    page.locator("input[name='email']").nth(1).fill(email)
    page.get_by_role("button", name="Signup").click()

    # 3. Check that the account-information page opens.
    expect(page.get_by_text("ENTER ACCOUNT INFORMATION")).to_be_visible()

    # 4. Fill in the required account and address details.
    page.locator("#id_gender1").check()
    page.locator("#password").fill(password)
    page.locator("#days").select_option("10")
    page.locator("#months").select_option("5")
    page.locator("#years").select_option("1990")
    page.locator("#first_name").fill("Tommy")
    page.locator("#last_name").fill("Lee")
    page.locator("#address1").fill("1 Via")
    page.locator("#country").select_option(label="United States")
    page.locator("#state").fill("California")
    page.locator("#city").fill("San Jose")
    page.locator("#zipcode").fill("95351")
    page.locator("#mobile_number").fill("+1117778889")

    # 5. Create the account and check the success message.
    page.get_by_role("button", name="Create Account").click()
    expect(page.get_by_text("ACCOUNT CREATED!")).to_be_visible()

    
