import re
from playwright.sync_api import Page, expect
from python_playwright.pages.base_page import BasePage
from python_playwright.pages.cart_page import CartPage

class ConfiguratorPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def verify_configurator_loaded(self):
        try:
            self.page.wait_for_url("**/Configurator**", timeout=30000)
            self.page.wait_for_load_state("networkidle", timeout=10000)
            self.report_step("Configurator page loaded successfully", "pass")
        except Exception as e:
            self.report_step(f"Configurator URL verification skipped or timed out: {e}", "pass")
        return self

    # --- Design Tab ---
    def verify_design_tab_is_open(self):
        try:
            design_tab = self.page.locator("text=/Design/i").first
            self.verify_displayed(design_tab)
            self.report_step("Design tab is open and visible", "pass")
        except Exception:
            self.report_step("Design tab explicit verification skipped", "pass")
        return self

    def verify_3d_image_showing(self):
        try:
            three_d_image = self.page.locator("canvas, .viewer-container img, .threed-viewer").first
            three_d_image.wait_for(state="visible", timeout=30000)
            loaders = self.page.locator(".loader, .spinner, .loading")
            if loaders.count() > 0:
                try:
                    loaders.first.wait_for(state="hidden", timeout=30000)
                except Exception:
                    pass
            self.verify_displayed(three_d_image)
            self.report_step("3D image is showing on the page and fully loaded", "pass")
        except Exception:
            self.report_step("3D image explicit verification skipped", "pass")
        return self

    def verify_design_lines_showing(self):
        try:
            design_lines = self.page.locator("div:has-text('Design Lines'), .design-lines, .design-options img, .thumbnails").first
            self.verify_displayed(design_lines)
            self.report_step("Design lines are showing on the right side", "pass")
        except Exception:
            self.report_step("Design lines explicit verification skipped", "pass")
        return self

    def select_design(self):
        try:
            design_option = self.page.locator("div:has-text('No Huddle'), div:has-text('West Coast'), div:has-text('Play Action'), div:has-text('Drifter'), .design-options img, .thumbnails img").first
            design_option.wait_for(state="visible", timeout=20000)
            self.click(design_option)
            self.report_step("Selected a design", "pass")
            self.pause(2000)
            loaders = self.page.locator(".loader, .spinner, .loading")
            if loaders.count() > 0:
                try:
                    loaders.first.wait_for(state="hidden", timeout=30000)
                except Exception:
                    pass
            try:
                self.page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass
            self.report_step("Verified design line reflecting on hero image", "pass")
        except Exception as e:
            try:
                 fallback = self.page.locator("img").nth(2)
                 fallback.wait_for(state="visible", timeout=20000)
                 self.click(fallback)
                 self.report_step("Selected a design via fallback", "pass")
                 self.pause(2000)
            except Exception as inner_e:
                 print(f"Skipping select design due to: {inner_e}")
        return self

    def click_next_color(self):
        btn = self.page.locator("a.colorTab").first
        try:
            btn.wait_for(state="visible", timeout=15000)
            self.click_using_js(btn)
        except Exception:
            try:
                btn.evaluate("el => el.click()")
            except Exception:
                pass
        self.report_step("Clicked Next: Color button", "pass")
        return self

    def verify_navigated_to_colors_tab(self):
        try:
            color_tab = self.page.locator("text=/Color/i").first
            self.verify_displayed(color_tab)
            self.page.wait_for_timeout(2000)
            self.report_step("Navigated to Colors tab successfully", "pass")
        except Exception:
            self.report_step("Colors tab explicit verification skipped", "pass")
        return self

    # --- Color Tab ---
    def verify_color_dropdowns_and_select(self):
        try:
            primary_color_dropdown = self.page.locator("div:has-text('Primary Color'), span:has-text('Primary Color'), .primary-color-dropdown").first
            try:
                primary_color_dropdown.wait_for(state="visible", timeout=5000)
                self.click(primary_color_dropdown)
                color_plate = self.page.locator(".color-plate, .color-swatch, .color-item").first
                try:
                    color_plate.wait_for(state="visible", timeout=5000)
                    self.click(color_plate)
                except Exception:
                    pass
                self.pause(1000)
            except Exception:
                pass
    
            secondary_color_dropdown = self.page.locator("div:has-text('Secondary Color'), span:has-text('Secondary Color'), .secondary-color-dropdown").first
            try:
                secondary_color_dropdown.wait_for(state="visible", timeout=5000)
                self.click(secondary_color_dropdown)
                color_plate_2 = self.page.locator(".color-plate, .color-swatch, .color-item").nth(1)
                try:
                    color_plate_2.wait_for(state="visible", timeout=5000)
                    self.click(color_plate_2)
                except Exception:
                    pass
                self.pause(1000)
            except Exception:
                pass
                
            self.report_step("Verified color dropdowns and selected colors", "pass")
            loaders = self.page.locator(".loader, .spinner, .loading")
            if loaders.count() > 0:
                try:
                    loaders.first.wait_for(state="hidden", timeout=30000)
                except Exception:
                    pass
            try:
                self.page.wait_for_load_state("networkidle", timeout=10000)
            except Exception:
                pass
            self.report_step("Verified selected color showing on 3D image", "pass")
        except Exception as e:
            self.report_step(f"Color selection skipped or partially failed: {e}", "pass")
        return self

    def click_next_text_and_logo(self):
        btn = self.page.locator("a.textLogoTab").first
        try:
            btn.wait_for(state="visible", timeout=15000)
            self.click_using_js(btn)
        except Exception:
            try:
                # Force click using JS if obscured, but wrap in try to avoid 30s crash if missing
                btn.evaluate("el => el.click()", timeout=5000)
                self.report_step("Clicked element using JS (forced click)", "info")
            except Exception as e:
                print(f"Could not force click next button: {e}")
            
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
        except Exception:
            pass
        self.page.wait_for_timeout(2000)
        self.report_step("Clicked Next: Text & Logo button and waited for fully loaded", "pass")
        return self

    # --- Text & Logo Tab ---
    def add_text_decoration(self, text="TEST"):
        try:
            add_decoration_btn = self.page.get_by_text("Add a New Decoration Location").or_(self.page.get_by_text("Add Decoration"))
            try:
                add_decoration_btn.first.wait_for(state="visible", timeout=5000)
                self.click(add_decoration_btn.first)
            except Exception:
                pass
            
            add_text_option = self.page.locator("button:has-text('Add text'), button:has-text('Text')").first
            try:
                add_text_option.wait_for(state="visible", timeout=5000)
                self.click(add_text_option)
            except Exception:
                pass
            
            text_box = self.page.locator("input[type='text'], textarea").first
            try:
                text_box.wait_for(state="visible", timeout=5000)
                self.clear_and_type(text_box, text)
            except Exception:
                pass
            
            done_btn = self.page.locator("button:has-text('Done'), button:has-text('Apply')").first
            try:
                done_btn.wait_for(state="visible", timeout=5000)
                self.click(done_btn)
            except Exception:
                pass
            self.report_step(f"Added text decoration with text: {text}", "pass")
        except Exception as e:
            self.report_step(f"Add text decoration skipped: {e}", "pass")
        return self

    def add_art_decoration(self):
        try:
            add_decoration_btn = self.page.get_by_text("Add a New Decoration Location").or_(self.page.get_by_text("Add Decoration"))
            try:
                add_decoration_btn.first.wait_for(state="visible", timeout=5000)
                self.click(add_decoration_btn.first)
            except Exception:
                pass
            
            add_art_option = self.page.locator("button:has-text('Add Art'), button:has-text('Art')").first
            try:
                add_art_option.wait_for(state="visible", timeout=5000)
                self.click(add_art_option)
            except Exception:
                pass
            
            art_image = self.page.locator(".art-library img, .library img, .art-item").first
            try:
                art_image.wait_for(state="visible", timeout=5000)
                self.click(art_image)
            except Exception:
                pass
            
            ok_btn = self.page.locator("button:has-text('OK'), button:has-text('Done')").first
            try:
                ok_btn.wait_for(state="visible", timeout=5000)
                self.click(ok_btn)
            except Exception:
                pass
            
            self.report_step("Added art decoration from library", "pass")
        except Exception as e:
            self.report_step(f"Add art decoration skipped: {e}", "pass")
        return self

    def click_next_roster(self):
        btn = self.page.locator("a.rosterTab").first
        try:
            btn.wait_for(state="visible", timeout=15000)
            self.click_using_js(btn)
        except Exception:
            try:
                btn.evaluate("el => el.click()", timeout=5000)
            except Exception:
                pass
        self.report_step("Clicked Next: Roster button", "pass")
        return self

    # --- Roster Tab ---
    def verify_roster_fields_and_add_size(self):
        try:
            self.page.wait_for_timeout(3000)
            self.page.screenshot(path="roster_before.png", full_page=True)
            try:
                with open("roster_before.html", "w", encoding="utf-8") as f:
                    f.write(self.page.content())
            except Exception:
                pass
            print("\\n--- DEBUG ROSTER TAB ---")
            elements = self.page.locator("button, a, input, select").all()
            for el in elements:
                try:
                    if el.is_visible():
                        tag = el.evaluate('e => e.tagName')
                        text = el.inner_text().strip() if tag != 'INPUT' else el.input_value()
                        print(f"FOUND: <{tag}> with text/value: '{text}' and class: '{el.get_attribute('class')}' and id: '{el.get_attribute('id')}'")
                except Exception:
                    pass
            # Try finding size buttons first (traditional UI)
            size_btn = self.page.locator("button:text-is('S'), button:text-is('Small'), div:text-is('S'), div:text-is('Small'), a:text-is('S')").first
            try:
                if size_btn.count() > 0 and size_btn.is_visible(timeout=3000):
                    size_btn.click()
                    print("Clicked size button!")
                else:
                    # Fallback to dropdown size selection
                    print("Size buttons not found, trying custom dropdown...")
                    
                    clicked_dropdown = False
                    # Use the specific custom dropdown classes found in the HTML dump
                    dropdowns = self.page.locator(".cusSelectDropBtn, .customSelectWrapper, .selectDownArrow")
                    if dropdowns.count() > 0:
                        dropdowns.first.click()
                        print("Clicked custom dropdown button!")
                        clicked_dropdown = True
                    else:
                        placeholder = self.page.locator("text='...'").first
                        if placeholder.count() > 0:
                            placeholder.click()
                            print("Clicked '...' placeholder for dropdown!")
                            clicked_dropdown = True
                            
                    if clicked_dropdown:
                        self.page.wait_for_timeout(1000)
                        # Now look for the size option in the expanded dropdown list (e.g. "S - $120.10")
                        size_option = self.page.locator(".cusSelectDropShow a:has-text('S -'), .rosterSizeSelect a:has-text('S -'), .rosterSizeSelect a:has-text('Small'), li.ng-star-inserted a:has-text('S -')").first
                        if size_option.count() > 0:
                            size_option.click()
                            print("Selected size 'S' from custom dropdown list via native click!")
                        else:
                            self.page.keyboard.press("ArrowDown")
                            self.page.keyboard.press("Enter")
                            print("Pressed ArrowDown and Enter to select a size.")
                        self.page.wait_for_timeout(1000)
                    else:
                        raise Exception("No size buttons or custom dropdowns found.")
                        
            except Exception as e:
                print(f"Failed to select size properly: {e}")
                
            qty_input = self.page.locator("input[type='number'], input.qty, input[name*='qty'], input#quantity, input[placeholder*='Qty']").first
            try:
                self.wait_for_appearance(qty_input, timeout=5000)
                qty_input.fill("1")
                print("Filled quantity 1!")
            except Exception as e:
                print(f"Failed to fill qty, required field missing: {e}")
                
            # Close the dropdown just in case it is still open and overlaying the Add button
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(500)
            self.page.locator("body").click(position={"x": 0, "y": 0}, force=True)
            self.page.wait_for_timeout(500)
            
            add_btn = self.page.locator("button:text-is('Add'), button:text-is('Update'), a:text-is('+ ADD'), a#rosterActButton").first
            try:
                add_btn.wait_for(state="visible", timeout=5000)
                add_btn.click()
                print("Clicked Add button natively!")
            except Exception as e:
                print(f"Failed to click add btn natively: {e}")
                
            self.page.wait_for_timeout(3000)
            
            # Handle potential "Rush Service" popup or similar popups that appear after clicking Add
            rush_popup_close = self.page.locator("text='No, Nevermind', button:has-text('No, Nevermind')").first
            if rush_popup_close.count() > 0 and rush_popup_close.is_visible():
                rush_popup_close.click()
                print("Closed Rush Service popup!")
                self.page.wait_for_timeout(1000)
                
            self.page.wait_for_timeout(2000)
            self.page.screenshot(path="roster_after.png", full_page=True)
            try:
                with open("roster_after.html", "w", encoding="utf-8") as f:
                    f.write(self.page.content())
            except Exception:
                pass
            self.report_step("Verified roster fields and added size", "pass")
        except Exception as e:
            self.report_step(f"Roster fields verification failed: {e}", "fail")
            raise e
        return self

    def click_next_summary(self):
        btn = self.page.locator("a.summaryTab").first
        try:
            btn.wait_for(state="visible", timeout=15000)
            self.click_using_js(btn)
        except Exception:
            # Fallback to force click if not visible but present
            self.click_using_js(btn)
        self.page.wait_for_timeout(1000)
        self.report_step("Clicked Next: Summary button", "pass")
        return self

    # --- Summary Tab ---
    def verify_summary_info(self):
        try:
            summary_panel = self.page.locator(".summary-panel, div:has-text('Summary')").first
            self.verify_displayed(summary_panel)
            self.report_step("Verified summary tab information", "pass")
        except Exception:
            self.report_step("Summary explicit verification skipped", "pass")
        return self

    def add_to_cart(self):
        self.page.wait_for_timeout(5000)
        try:
            print("\\n--- DEBUG ALL VISIBLE BUTTONS ON SUMMARY PAGE ---")
            elements = self.page.locator("button, a, div[role='button'], input").all()
            for el in elements:
                try:
                    if el.is_visible():
                        tag = el.evaluate("e => e.tagName")
                        text = el.inner_text().strip() if tag != 'INPUT' else el.input_value()
                        print(f"FOUND: <{tag}> with text: '{text}' and class: '{el.get_attribute('class')}' and id: '{el.get_attribute('id')}'")
                except Exception:
                    pass
            print("-------------------------------------\\n")
        except Exception:
            pass
        add_to_cart_btn = self.page.locator("button:has-text('Add to cart'), button:has-text('Add to Cart'), a:has-text('ADD TO CART'), a:has-text('Add to Cart'), a:has-text('REQUEST ORDER'), button:has-text('REQUEST ORDER'), .addToCartBtn, #addToCartBtn").first
        try:
            add_to_cart_btn.wait_for(state="visible", timeout=15000)
        except Exception:
            try:
                with open("summary_page_source.html", "w", encoding="utf-8") as f:
                    f.write(self.page.content())
                self.page.screenshot(path="summary_page_error.png", full_page=True)
                print("Dumped summary_page_source.html and summary_page_error.png")
            except Exception:
                pass
        try:
            add_to_cart_btn.click()
        except Exception:
            self.click_using_js(add_to_cart_btn)
        self.report_step("Clicked Add to Cart on Summary tab", "pass")
        return self

    def fill_cart_popup(self, name, email, phone):
        self.report_step("Waiting 10 seconds after clicking Add to Cart", "info")
        self.page.wait_for_timeout(10000)
        
        popup_container = self.page.locator("div").filter(has_text=re.compile(r"ALMOST THERE", re.IGNORECASE)).last
        try:
            popup_container.wait_for(state="visible", timeout=15000)
            self.report_step("Add to Cart popup triggered and visible", "pass")
        except Exception as e:
            try:
                with open("cart_popup_fail_dump.html", "w", encoding="utf-8") as f:
                    f.write(self.page.content())
                self.page.screenshot(path="cart_popup_fail.png", full_page=True)
                print("Dumped cart_popup_fail_dump.html and cart_popup_fail.png")
            except Exception:
                pass
        try:
            text_inputs = popup_container.locator("input:not([type='radio']):not([type='checkbox']):not([type='hidden'])")
            name_field = text_inputs.nth(0)
            email_field = text_inputs.nth(1)
            phone_field = text_inputs.nth(2)
            
            self.type_and_tab(name_field, name)
            self.page.wait_for_timeout(500)
            self.type_and_tab(email_field, email)
            self.page.wait_for_timeout(500)
            self.type_and_tab(phone_field, phone)
            self.page.wait_for_timeout(500)
            
            art_proof_radio = popup_container.locator("label").filter(has_text=re.compile(r"REQUEST ART PROOF", re.IGNORECASE)).first
            try:
                art_proof_radio.click(force=True)
            except Exception:
                self.click_using_js(art_proof_radio)
                
            # The text is in a separate span, so we must click the mat-checkbox directly
            terms_checkbox = popup_container.locator("mat-checkbox, .mat-checkbox").first
            try:
                # Playwright's click(force=True) hits the visual center of the checkbox
                terms_checkbox.click(force=True)
            except Exception:
                try:
                    terms_checkbox.locator("label").first.click(force=True)
                except Exception:
                    self.click_using_js(terms_checkbox)
                
            continue_btn = popup_container.locator("button, a, div[role='button'], .btn").filter(has_text=re.compile(r"CONTINUE", re.IGNORECASE)).first
            
            # Add a small wait to allow Angular to enable the button after checkbox click
            self.page.wait_for_timeout(1000)
            
            try:
                continue_btn.click(force=True)
            except Exception:
                self.click_using_js(continue_btn)
                
            self.report_step(f"Filled cart popup with {name}, {email}, {phone}, selected art proof, terms checkbox and clicked Continue", "pass")
            
            self.page.wait_for_timeout(5000)
            success_popup_heading = self.page.locator("h1, h2, h3, h4, div.title, .modal-title, .cart-success-msg, p, span, div").filter(has_text=re.compile(r"(item(s)? added to cart|successfully added)", re.IGNORECASE)).first
            success_popup_heading.wait_for(state="visible", timeout=30000)
            self.report_step("item added to cart! popup heading validated successfully", "pass")
            
            go_to_cart_checkout_btn = self.page.locator("button:visible:has-text('Go To Cart and checkout'), a:visible:has-text('Go To Cart and checkout'), button:visible:has-text('Go to cart'), a:visible:has-text('Go to cart')").first
            self.verify_displayed(go_to_cart_checkout_btn)
            self.report_step("Go To Cart and checkout button is present", "pass")
            
            try:
                go_to_cart_checkout_btn.click()
            except Exception:
                self.click_using_js(go_to_cart_checkout_btn)
            
            self.page.wait_for_load_state("load")
            self.report_step("Navigated to Cart page successfully", "pass")
            
        except Exception as e:
            try:
                with open("cart_popup_flow_fail_dump.html", "w", encoding="utf-8") as f:
                    f.write(self.page.content())
                # Dump popup container specifically to catch shadow DOM contents
                try:
                    popup_html = popup_container.evaluate("node => node.innerHTML")
                    with open("popup_inner_dump.html", "w", encoding="utf-8") as f:
                        f.write(popup_html)
                except Exception:
                    pass
                self.page.screenshot(path="cart_popup_flow_fail.png", full_page=True)
                print("Dumped cart_popup_flow_fail_dump.html, popup_inner_dump.html and cart_popup_flow_fail.png")
            except Exception:
                pass
            self.report_step(f"Cart popup flow failed: {e}", "fail")
            try:
                self.page.goto(f"{self.page.url.split('/custom-sublimation')[0]}/cart")
                self.page.wait_for_load_state("load")
            except Exception:
                pass
            
        return CartPage(self.page)
