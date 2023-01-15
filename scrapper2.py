import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# specify the URL of the website
url = 'https://www.betika.com/en-ke/s/soccer'
# set headers 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'}

response = requests.get(url)

# check if the page is dynamic
if "no-js" in response.text:
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
        #myDiv = driver.find_element(By.CLASS_NAME, 'prebet-match')
        #print(myDiv.text)

        # parse the HTML content of the website
        soup = BeautifulSoup(html, 'html.parser')

        # find all elements with the class 'pre-bet match'
        matches = soup.find_all("div", class_='prebet-match')

        # iterate through the matches and print the text
        teams = []
        odds = []
        for match in matches:    
            #print(match.text)
            time = match.find('div', {'class': 'time'}).text
            home = match.find('span', {'class': 'prebet-match__teams__home'}).text
            teams = match.find('div', {'class': 'prebet-match__teams'}).text
            away = lambda x: x.replace(home, '').strip()
            #odds.append(match.find('span', {'class': 'prebet-match__odd__odd-value'}).text)
            #odd =  lambda listx: [print(x) for x in listx]
            

            print(time.strip())
            print(home.strip())
            print(away(teams))
            #print(odds[0].text.strip())

    except Exception as e:
        print(f'An error occurred: {e}')

    finally:
        # close the browser
        driver.quit()

else:
    try:
        # send a GET request to the website and store the response
        response = requests.get(url, headers=headers)

        # parse the HTML content of the website
        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)

        # find all elements with the class 'pre-bet match'
        matches = soup.find_all("div", class_='pre-bet match')

        # iterate through the matches and print the text
        for match in matches:
            print(match.text)
            print('---------------------')
    except requests.exceptions.RequestException as e:
        # handle error
        print(f'An error occurred: {e}')
