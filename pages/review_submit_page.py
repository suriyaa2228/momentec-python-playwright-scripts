from python_playwright.pages.base_page import BasePage, Locators
from python_playwright.pages.thank_you_page import ThankYouPage

class ReviewSubmitPage(BasePage):
    def click_place_order(self):
        strategies = [
            "(//div[contains(text(),'PLACE ORDER')])[2]",
            "//div[translate(text(), 'place ord', 'PLACE ORD')='PLACE ORDER']",
            "//button[contains(text(),'Place Order') or contains(text(),'PLACE ORDER')]",
            "//div[contains(@class, 'place-order') or contains(@class, 'submit-order')]",
            "//button[@id='placeOrderBtn']",
            "//input[@value='Place Order' or @value='PLACE ORDER']"
        ]
        btn = None
        for strategy in strategies:
            try:
                el = self.page.locator(f"xpath={strategy}").first
                if el.is_visible(timeout=5000):
                    btn = el
                    break
            except Exception:
                pass
                
        if not btn:
            # Try to find any element with text "Place Order"
            try:
                el = self.page.locator("text=/Place Order/i").first
                if el.is_visible(timeout=5000):
                    btn = el
            except Exception:
                pass

        if btn:
            self.scroll_to_element(btn)
            self.click(btn)
            self.report_step("Place Order Button get clicked Successfully", "pass")
        else:
            with open("review_submit_dump.html", "w", encoding="utf-8") as f:
                f.write(self.page.content())
            self.report_step("Place Order Button not found", "fail")
            
        return ThankYouPage(self.page)
