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

# Find the <ul> tag containing all the product information
ul_tag = soup.find('ul', class_='results-base')

# Find all <li> tags within the <ul> tag
product_list_items = ul_tag.find_all('li', class_='product-base')

# Iterate over each <li> tag to scrape product information
for li_tag in product_list_items:
    o = {}  # Create a new dictionary for each product
    try:
        o["Product Brand"] = li_tag.find('h3', class_='product-brand').text.strip()
    except:
        o["Product Brand"] = None
    try:
        o["Product Name"] = li_tag.find('h4', class_='product-product').text.strip()
    except:
        o["Product Name"] = None
    try:
        # Extract product price text
        price_text = li_tag.find('div', class_='product-price').find('span', class_='product-discountedPrice').text.strip()
        # Convert product price to numerical value
        o["Product Price"] = float(price_text.replace('Rs.', '').replace(',', ''))
    except:
        o["Product Price"] = None
    try:
        o["Product Ratings"] = float(li_tag.find('div', class_='product-ratingsContainer').find('span').text.strip())
    except:
        o["Product Ratings"] = None
    try:
        # Extract raw ratings count string
        ratings_count_raw = li_tag.find('div', class_='product-ratingsCount').text.strip()
        # Process the ratings count string
        if '|' in ratings_count_raw:
            ratings_count = ratings_count_raw.split("|")[1].strip()
        else:
            ratings_count = ratings_count_raw
        # Convert number of people who have rated the product to numerical value
        if 'k' in ratings_count:
            o["Number of People have rated this product"] = float(ratings_count.replace('k', '')) * 1000
        else:
            o["Number of People have rated this product"] = float(ratings_count)
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
