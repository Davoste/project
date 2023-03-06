# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 16:26:55 2022

@author: HP 840
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time


#Starts the driver and goes to our starting webpage
driver = webdriver.Chrome(
    'C:/Users/HP 840/chromedriver.exe'
)

driver.get('https://www.indeed.com/')

#Inputs a job title into the input box
input_box = driver.find_element(By.XPATH,'//*[@id="text-input-what"]')
input_box.send_keys('data analyst')

#Clicks on the search button
button = driver.find_element(By.XPATH,'//*[@id="jobsearch"]/button').click()

#Creates a dataframe
df = pd.DataFrame({'Link':[''], 'Job Title':[''], 'Company':[''], 'Location':[''],'Salary':[''], 'Date':['']})

#This loop goes through every page and grabs all the details of each posting
#Loop will only end when there are no more pages to go through
while True:  
    #Imports the HTML of the current page into python
    soup = BeautifulSoup(driver.page_source, 'lxml')
    
    #Grabs the HTML of each posting
    postings = soup.find_all('div', class_ = 'job_seen_beacon')
    
    #grabs all the details for each posting and adds it as a row to the dataframe
    for post in postings:
        link = post.find('a', class_ = 'jcs-JobTitle css-jspxzf eu4oa1w0').get('href')
        link_full = 'https://www.indeed.com'+link
        name = post.find('div', class_ = 'css-1m4cuuf e37uo190').text.strip()
        company = post.find('span', class_ = 'companyName').text.strip()
        try:
            location = post.find('div', class_ = 'companyLocation').text.strip()
        except:
            location = 'N/A'
        date = post.find('span', class_ = '').text.strip()
        try:
            salary = post.find('span', class_ = 'salaryText').text.strip()
        except:
            salary = 'N/A'
        df = df.append({'Link':link_full, 'Job Title':name, 'Company':company, 'Location':location,'Salary':salary, 'Date':date},
                       ignore_index = True)
    
    #checks if there is a button to go to the next page, and if not will stop the loop
    try:
        button = soup.find('a', attrs = {'aria-label': 'Next'}).get('href')
        driver.get('https://www.indeed.com'+button)
    except:
        break

