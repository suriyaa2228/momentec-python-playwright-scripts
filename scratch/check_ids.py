from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # directly navigate to the product URL
        page.goto("https://stage.momentecbrands.com/search?q=295000")
        page.wait_for_load_state("networkidle")
        
        # Click the product link if we are on search page
        product_link = page.locator("a.product_name").first
        if product_link.is_visible():
            product_link.click()
            page.wait_for_load_state("networkidle")
            
        print("URL:", page.url)
        print("Title:", page.title())
        
        # select black
        black = page.locator("//img[contains(@alt,'Black')]").first
        if black.is_visible():
            black.click(force=True)
            page.wait_for_timeout(2000)
            
        ids = page.evaluate("Array.from(document.querySelectorAll('div[id]')).map(el => el.id).filter(id => id.includes('grid'))")
        print("Div IDs containing grid:", ids)
        
        qty = page.locator("input[type='number']").first
        if qty.is_visible():
            print("Found number input")
            parent = qty.evaluate("el => { let p = el.closest('div[id]'); return p ? p.id : null; }")
            print("Parent div ID:", parent)
            
        browser.close()

if __name__ == "__main__":
    run()
