import requests
import os
import re
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# specify the URL of the website
url = 'https://odibets.com/'
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
    # print(soup.prettify())

    # find all elements with the class 'pre-bet match'
    matches = soup.find_all("div", class_='l-games-event')

    # iterate through the matches and print the text    
    
    for match in matches: 
        # print(match.prettify())
        # time = match.select('a span:first-child')
        time = match.find("div", class_='m').find_all('span')[-3].text

        for link in match.find('a',{'class': 'inf'}):
            teams = match.find_all('div', {'class': 't-i'})
        home = teams[0].text
        away = teams[1].text

        # Find the odds
        for button in match.find('div', {'class': 'mar-cont'}):
            odds = match.find_all('span', class_='b')
        H = odds[0].text
        X = odds[1].text
        A = odds[2].text

        # store the data in a dictionary
        data.append({
        'time': time,
        'home': home,
        'away': away,
        'H': H,
        'X': X,
        'A': A
        })

    df = pd.DataFrame(data)
    print(df)

except Exception as e:
    print(f'An error occurred: {e}')

finally:
    # close the browser
    driver.quit()