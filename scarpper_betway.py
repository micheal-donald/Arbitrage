import requests
import os
import re
import pandas as pd
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
# def scrap_betika():
# specify the URL of the website
url = 'https://www.betway.co.ke/sport/soccer'
# set headers 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'}

response = requests.get(url)

# Create an empty list to store the extracted data
data = []

# check if the page is dynamically loaded
# Instantiate options
chrome_options = Options()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--remote-debugging-port=9222")
chrome_options.add_argument("--headless")
# Set the location of the webdriver
chrome_driver = os.getcwd() + "chromedriver.exe"
service = webdriver.chrome.service.Service(chrome_driver)
service.start()
# create a new instance of the Firefox driver
# Instantiate a webdriver
driver = webdriver.Remote(service.service_url, options=chrome_options)

try:

    # navigate to the website
    driver.get(url)

    # wait for the page to load
    driver.implicitly_wait(10)

    # get the HTML content of the page
    html = driver.page_source

    # parse the HTML content of the website
    soup = BeautifulSoup(html, 'html.parser')


    # Find the elements with the class 'row eventRow'
    matches = soup.find_all("class", class_='row eventRow')

    # iterate through the matches and print the text

    for match in matches:
        league = match.find('div', class_='teams-info-meta-left').text.strip()
        time = match.find('div', class_='teams-info-meta-right').text.strip()
        teams_list = match.find_all('div', class_='teams-info-vert-top')
        for team in teams_list:
            teams = match.find_all('div', class_='teams-info-vert-top')
            H = teams[0].text.strip()
            A = teams[1].text.strip()
        for odds in match.find_all('div', class_='odds__value'):
            odds = match.find_all('div', class_='odds__value')
            Yes = odds[0].text.strip()
            No = odds[1].text.strip()
        
        #store the data in a dictionary
        data.append({
            'league': league,
            'time': time,
            'H': H,
            'A': A,
            'Yes': Yes,
            'No': No
        })

    df_betk_btts=pd.DataFrame(data)
    #clean leading and trailing spaces
    df_betk_btts = df_betk_btts.applymap(lambda x: x.strip() if isinstance(x, str) else x)   
    #Save data with Pickle
    output = open('df_betk_btts', 'wb')
    pickle.dump(df_betk_btts, output)
    output.close()
    #return df_betk  
     
except Exception as e:
    print(f'An error occurred: {e}')

finally:
    # close the browser
    driver.quit()