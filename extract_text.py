from bs4 import BeautifulSoup

with open("c:/Users/SuriyaaP/momentecautomation/Momentec_Automation/python_playwright/cart_popup_flow_fail_dump.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
text = soup.get_text(separator=' ', strip=True)
print(text[:2000])
