from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


driver=webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get("https://www.myntra.com/women-tops")
html_content = driver.page_source
print(html_content)
# Close the browser
driver.quit()