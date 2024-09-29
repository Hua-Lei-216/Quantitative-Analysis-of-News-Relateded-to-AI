# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 10:11:37 2024

@author: 睢旸
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Initialize Edge driver
driver = webdriver.Edge()

# Get the unchanged target URL
driver.get('https://search.people.cn/s?keyword=人工智能&st=0&_=1727526726346')

file_data = []

# Traverse the first 100-page
for page in range(1, 101):
    print(f"Crawling page {page}")
    
    locators = [
        (By.CSS_SELECTOR, "li.clear.img-li"),
        (By.CSS_SELECTOR, "li.clear")  
    ]
    
    for loco in locators:
        try:
            # Wait for page elements to load
            WebDriverWait(driver, 40).until(
                EC.presence_of_element_located(loco)
            )
            
            # Find all news items
            news_items = driver.find_elements(loco[0], loco[1])
    
            # Traverse each news item to extract information
            for item in news_items:
                try:
                    # Extract titles and links
                    title_element = item.find_element(By.CSS_SELECTOR, "div.ttl a")
                    title = title_element.text
                    link = title_element.get_attribute("href")
        
                    # Extract summary
                    summary = item.find_element(By.CSS_SELECTOR, "div.content").text
                    
                    # Extract date
                    pub_date = item.find_element(By.CSS_SELECTOR, "div.fot").text
        
                    # Print or store information
                    print(f"Title: {title}")
                    print(f"Link: {link}")
                    print(f"Summary: {summary}")
                    print(f"Publication Date: {pub_date}")
                    print("="*50)
                    
                    file_data.append({
                        'News Title': title,
                        'Publication Date': pub_date,
                        'News Summary': summary,
                        'News Link': link
                    })
                    
                except Exception as e:
                    print(f"Error extracting information from news item: {e}")
        except Exception as e:
            print(f"Error waiting for news items: {e}")
    
    # Click the next page button to simulate page turning
    try:
        # Scroll to the bottom of the page to ensure that all elements are loaded
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait for the next page button to click to update the positioning structure
        next_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span.page-next"))
        )
        
        # Click next page
        next_button.click()
    
        # Wait for the page to load new content, dynamic wait
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "li.clear"))
        )
    except Exception as e:
        print(f"Page turning failed: {e}")
        break  # If the page cannot be flipped, exit

# Quit driver
driver.quit()

# Save the data to excel under the target path
df = pd.DataFrame(file_data)
df.to_excel("D:/rmw_ai_pages.xlsx", index=False)
print("Data already saved to rmw_ai_pages.xlsx")