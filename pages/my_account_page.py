from python_playwright.pages.base_page import BasePage, Locators

class MyAccountPage(BasePage):
    def verify_dashboard(self):
        title_element = self.locate_element(Locators.XPATH, "//h3[@class=\"AccPgeSubTitle\"]")
        self.verify_displayed(title_element)
        text = self.get_element_text(title_element)
        if text.lower() == "dashboard":
            self.report_step(f"Page successfully landed on {text} page", "pass")
        else:
            self.report_step(f"Landed on different title: expected 'dashboard', got '{text}'", "fail")
        return self
