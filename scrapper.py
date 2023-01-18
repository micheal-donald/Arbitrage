import requests
from bs4 import BeautifulSoup

# specify the URL of the Betika website
url = 'https://odibets.com/'

# set headers 
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0'}

try:
    # send a GET request to the website and store the response
    response = requests.get(url, headers=headers)

    # parse the HTML content of the website
    soup = BeautifulSoup(response.content, 'html.parser')

    # find all elements with the class 'pre-bet match'
    matches = soup.find_all("div", class_='l-games-event')

    # iterate through the matches and print the text
    for match in matches:
        print(match.text)
        print('---------------------')
except requests.exceptions.RequestException as e:
    # handle error
    print(f'An error occurred: {e}')
