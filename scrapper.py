import subprocess
import pandas as pd
import pickle
from fuzzywuzzy import process, fuzz
from sympy import symbols, Eq, solve
from scrapper_betika import scrap_betika
from scrapper_odi import scrap_odibets

def get_odds():
    # get the odds from the websites
    betika = scrap_betika()
    odibets = scrap_odibets()


get_odds()
    # create a dataframe from the odds
    # df = pd.DataFrame(betika, columns=['Time', 'Home', 'Away', 'Betika 1', 'Betika X', 'Betika 2'])
    # df2 = pd.DataFrame(odibets, columns=['Time', 'Home', 'Away', 'Odi 1', 'Odi X', 'Odi 2'])

