from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
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
    try:
        o["Product Ratings"] = soup.find_all('div', {'class': 'product-ratingsContainer'})[len(l)].find('span').text.strip()
    except:
        o["Product Ratings"] = None
    try:
        ratings_count = soup.find_all('div', {'class': 'product-ratingsCount'})[len(l)].text.strip()
        # Remove "|" character from ratings count
        o["Number of People have rated this product"] = ratings_count.split("|")[1].strip() if "|" in ratings_count else ratings_count.strip()
    except:
        o["Number of People have rated this product"] = None

    l.append(o)

# Print the list of product info
i = 1
for product in l:
    print(i, product)
    i+=1

# Save data to Excel file
wb = Workbook()
ws = wb.active

# Write headers
headers = ["Product Brand", "Product Name", "Product Price", "Product Ratings", "Number of People have rated this product"]
ws.append(headers)

# Write data
for product in l:
    ws.append([product.get(header, "") for header in headers])

# Save workbook
wb.save("productid.xlsx")
print("Data saved to productid.xlsx")

# Close the browser
driver.quit()
