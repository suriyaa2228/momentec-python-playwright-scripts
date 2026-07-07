from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://stage.momentecbrands.com/augusta-1"
        print("Navigating...")
        page.goto(url)
        
        # Accept cookies
        try:
            page.locator("button#onetrust-accept-btn-handler").click(timeout=5000)
        except Exception:
            pass
            
        print("Searching for 295000...")
        page.locator("id=SimpleSearchForm_SearchTerm").fill("295000")
        page.locator("id=searchFilterButton").click()
        page.wait_for_load_state("networkidle")
        
        print("Clicking product...")
        result = page.locator("(//span[contains(text(),'Style # 295000')])[2]")
        result.wait_for(state="visible", timeout=10000)
        
        # Get the URL of the product link or click it
        product_link = page.locator(f"//a[contains(@href, '295000')]").first
        if product_link.is_visible():
            product_link.click()
        else:
            print("Could not find product link to click")
            
        page.wait_for_load_state("networkidle")
        print("On PDP page. Title:", page.title())
        
        # Click black color
        print("Selecting black color...")
        black_thumbnail = page.locator("//img[contains(@alt,'Black')]").first
        if black_thumbnail.is_visible():
            black_thumbnail.click(force=True)
            page.wait_for_timeout(2000)
            
            # Now find the placeholder
            print("Dumping all div IDs...")
            ids = page.evaluate("Array.from(document.querySelectorAll('div[id]')).map(el => el.id).filter(id => id.includes('295000'))")
            print("Div IDs containing 295000:", ids)
            
            grids = page.evaluate("Array.from(document.querySelectorAll('div[id]')).map(el => el.id).filter(id => id.includes('grid'))")
            print("Div IDs containing grid:", grids)
            
            # Print the HTML of the quantity section
            qty_section = page.locator("//input[contains(@name, 'quantity') or contains(@id, 'quantity')]").first
            if qty_section.is_visible():
                parent_id = qty_section.evaluate("el => el.closest('div[id]') ? el.closest('div[id]').id : 'No parent with ID'")
                print("Quantity input is inside div with ID:", parent_id)
        else:
            print("Black color thumbnail not found")
        
        browser.close()

if __name__ == "__main__":
    run()
