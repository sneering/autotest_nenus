import time
from playwright.sync_api import sync_playwright
from logger import logger
from utils import take_screenshot, open_site, login_with_github, launch_workspace, chat_with_agent

# Test GitHub repo link
TEST_REPO = "https://github.com/imrahulr/adversarial_robustness_pytorch.git"

def run():

    steps_status = {
        "open": False,
        "login": False, 
        "workspace": False,
        "chat": False
    }

    with sync_playwright() as p:
        logger.info("Launching browser...")
        browser = p.chromium.launch(headless=False) # Set headless=True to hide the browser (run without UI)
        context = browser.new_context(storage_state="github_state.json") # saved login cookies/tokens 
        page = context.new_page()


        # Step 1: Open
        res_open = open_site(page)
        if res_open:
            steps_status["open"] = True
            logger.info("Step 1 (Open): SUCCESS")    
        else:
            logger.error(f"Step 1 (Open): FAILED")


        # Step 2: Login via GitHub
        res_login = login_with_github(page)
        if res_login: 
            steps_status["login"] = True
            logger.info("Step 2 (Login): SUCCESS")
        else:
            logger.error(f"Step 2 (Login): FAILED")


        # Step 3: Enter repo link and launch workspace
        res_launch, new_tab = launch_workspace(page, TEST_REPO)
        if res_launch:
            steps_status["workspace"] = True
            logger.info("Step 3 (Workspace): SUCCESS")
        else:
            logger.error(f"Step 3 (Workspace): FAILED")
            take_screenshot(page, "903_workspace_error")


        # Step 4: Initiate a chat with agent
        res_chat = chat_with_agent(new_tab, "Hello!")
        if res_chat:
            steps_status["chat"] = True
            logger.info("Step 4 (Chat): SUCCESS")
        else:
            logger.error(f"Step 4 (Chat): FAILED")
           

        # Summary:
        successful_steps = sum(steps_status.values())
        total_steps = len(steps_status)
        success_rate = (successful_steps / total_steps) * 100

        logger.info(f"SUMMARY:")
        print("SUMMARY:")
        logger.info(f"Successful steps: {successful_steps}/{total_steps}")
        print(f"Successful steps: {successful_steps}/{total_steps}")
        logger.info(f"Success rate: {success_rate:.1f}%")
        print(f"Success rate: {success_rate:.1f}%")
        
        browser.close()

if __name__ == "__main__":
    run()

