from playwright.sync_api import sync_playwright

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False
    )

    page = browser.new_page()

    page.goto("https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026/statistics")

    input("Press Enter to close...")

    browser.close()