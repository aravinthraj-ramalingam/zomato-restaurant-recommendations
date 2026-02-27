from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
driver = webdriver.Chrome(options=options)

driver.get("http://localhost:8080")
driver.find_element(By.ID, "place").send_keys("Banashankari")
driver.find_element(By.ID, "cuisine").send_keys("North Indian")
driver.find_element(By.CSS_SELECTOR, ".cta-btn").click()

try:
    WebDriverWait(driver, 15).until(
        lambda d: not d.find_element(By.ID, "results-content").get_attribute("class").__contains__("hidden") or \
                  not d.find_element(By.ID, "error-state").get_attribute("class").__contains__("hidden")
    )
except Exception:
    pass

with open('browser_logs.txt', 'w') as f:
    for log in driver.get_log("browser"):
        f.write(str(log) + '\n')

driver.quit()
