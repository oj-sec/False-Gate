from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.eservicebits.com/landingpages/fe996bbf-3dce-487c-acd3-4a69200fa8a0/iacxjd89fjfws0oixryzrvrs8z3sfspvh9wokt0qqn4")
    page.get_by_placeholder("someone@example.com").fill("abbbbb@inioneoinwfoeinfoweinfoinf.com")
    page.get_by_placeholder("someone@example.com").press("Tab")
    page.get_by_placeholder("Password").fill("pppppppppppppppppppppp")
    page.get_by_placeholder("Password").press("Enter")
    page.close()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
