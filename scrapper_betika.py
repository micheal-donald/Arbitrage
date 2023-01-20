import requests
import os
import re
import pandas as pd
import pickle
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def scrap_betika():
    # specify the URL of the website
    url = 'https://www.betika.com/en-ke/s/soccer'
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
    chrome_options.headless = True
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

        # find all elements with the class 'pre-bet match'
        matches = soup.find_all("div", class_='prebet-match')

        # iterate through the matches and print the text
        teams = []
        
        
        for match in matches:
                
            #print(match.text)
            time = re.sub(r"[\n\t]*", '', match.find('div', {'class': 'time'}).text)
            home = match.find('span', {'class': 'prebet-match__teams__home'}).text
            teams = match.find('div', {'class': 'prebet-match__teams'}).text
            get_away = lambda x: x.replace(home, '').strip()
            away = get_away(teams)
            odds_list = match.find_all('span', {'class': 'prebet-match__odd__odd-value bold'})
            for odd in odds_list:
                odds = match.find_all('span', {'class': 'prebet-match__odd__odd-value bold'})
                H = float(odds[0].text)
                X = float(odds[1].text)
                A = float(odds[2].text)

            # store the data in a dictionary
            data.append({
                'time': time,
                'home': home,
                'away': away,
                'H': H,
                'X': X,
                'A': A
            })
        df_betk = pd.DataFrame.from_dict(data)
        #clean leading and trailing whitespaces of all odds
        df_betk = df_betk.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        #Save data with Pickle
        output = open('df_betk', 'wb')
        pickle.dump(df_betk, output)
        output.close()
        #return df_betk

    except Exception as e:
        print(f'An error occurred: {e}')

    finally:
        # close the browser
        driver.quit()