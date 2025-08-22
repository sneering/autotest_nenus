from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Open GitHub Page
    page.goto("https://github.com/login")

    input("Please log in to GitHub")

    # Save session 
    context.storage_state(path="github_state.json")
    print("GitHub login state has been saved to github_state.json, plase run main.py to start test")
    browser.close()
