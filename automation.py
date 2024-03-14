from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

l = []

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

driver.get("https://www.myntra.com/women-tops")
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

# Finding individual product's info
while len(l) < 50:
    o = {}  # Create a new dictionary for each product
    try:
        o["Product Brand"] = soup.find_all('h3', {'class': 'product-brand'})[len(l)].text.strip()
    except:
        o["Product Brand"] = None
    try:
        o["Product Name"] = soup.find_all('h4', {'class': 'product-product'})[len(l)].text.strip()
    except:
        o["Product Name"] = None
    try:
        o["Product Price"] = soup.find_all('div', {'class': 'product-price'})[len(l)].find('span', {'class': 'product-discountedPrice'}).text.strip()
    except:
        o["Product Price"] = None

    l.append(o)

# Print the list of product info
for product in l:
    print(product)

# Close the browser
driver.quit()
