from playwright.sync_api import Playwright, sync_playwright, expect
from urllib.parse import urlparse
import time


# Runner routine
def run(playwright: Playwright, target, username, password, mfa=None) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    page.set_default_timeout(10000)

    stored_post_requests = []
    page.on("request", lambda request: stored_post_requests.append({"requestUrl":request.url, "postData":request.post_data}) if request.method == "POST" else None)
    
    page.goto(target)
    
    all_inputs = page.locator("input")
    try:
        try:
            all_inputs.nth(0).fill(username)
        except:
            try:
                body = page.locator("body")
                body.click()
                time.sleep(1)
                page.keyboard.down("Tab")
                time.sleep(1)
                page.keyboard.down("Enter")
                all_inputs.nth(0).fill(username)
                time.sleep(1)
            except:
                page.close()
                context.close()
                browser.close()
                return 1

        try: 
            time.sleep(1)
            all_inputs.nth(1).fill(password)
            time.sleep(1)
            page.keyboard.down("Enter")
            time.sleep(8)
        except:
            page.keyboard.down("Enter")
            all_inputs.nth(1).fill(password)
            page.keyboard.down("Enter")
            time.sleep(8)
    except:
        page.close()
        context.close()
        browser.close()
        return 1
    
    # TODO MFA handler 

    page.close()
    context.close()
    browser.close()

    return stored_post_requests

# Function to clean up post requests based on an ignore list
def post_domain_cleaner(stored_post_requests):
    
    cleaned_post_requests = []
    with open('post_domain_ignore_list', 'r') as f:
        ignore_domains = f.read().splitlines()
    for item in stored_post_requests:
        domain = urlparse(item['requestUrl'])
        if domain not in ignore_domains:
            cleaned_post_requests.append(item)

    return cleaned_post_requests

# Module entry point & main execution handler
def start(target, credentials):

    with sync_playwright() as playwright:
        stored_post_requests = run(playwright, target, credentials['username'], credentials['password'])

        if stored_post_requests == 1:
            return

    cleaned_post_requests = post_domain_cleaner(stored_post_requests)
            
    formatted_return = {}
    formatted_return['targetUrl'] = target
    formatted_return['credentialsUsed'] = credentials
    formatted_return['engagementRoutine'] = 'basic'
    formatted_return['postRequestsTriggered'] = cleaned_post_requests

    print(formatted_return)

    return formatted_return    


if __name__ == "__main__":

    # Testing credentials
    start("https://gateway.ipfs.io/ipfs/QmbLd37HqzS5Nid7yrwZVb3X28qYyVRtodF5U1gnBqTeC3", {"username":"bobbytables@gmail.com","password":"bongos99"})
