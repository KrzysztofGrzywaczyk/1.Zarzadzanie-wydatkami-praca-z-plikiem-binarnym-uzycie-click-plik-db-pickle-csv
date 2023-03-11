
""" 
A simple program that calculates the historical exchange rates of a given currency on a given date.
Based on official NBP rates from NBP API.
NBP Base does not publish rates on weekends and before 2002, the given date must meet these requirements.

Requirements:   currency - code ISO 4217 format (EUR,USD etc.), date - any format

Usage:  Aktualny_kurs_walut.py  currency date              

        ... or just type the values during the run of the program.
"""

# Demands API NBP:
# http://api.nbp.pl/api/exchangerates/rates/{tabela A,B,C}/{code}/{date}/?format=json
# date in format: RRRR-MM-DD

import sys

from datetime import datetime
from dateutil import parser
import requests
from requests.models import Response


def print_intro():
    print("-----------------------------------------------------------------------")
    print(" KURSY WALUT OBCYCH Z WYBRANEGO DNIA :")
    print("-----------------------------------------------------------------------")


def get_currency() -> str:
    try:
        currency = sys.argv[1]
    except IndexError:
        currency = input("Wprowadź walutę obcą:  ")
    return currency


def get_date() -> str:
    try:
        date = sys.argv[2]
    except IndexError:
        date = input("wprowadź datę:   ")
    return date


def parse_date(date :str) -> datetime:
    """Creates a datetime object from any string date."""

    try:
        parsed_date = parser.parse(date)
    except:
        print_error('date')
        sys.exit(12)
    return parsed_date


def print_error(err_name:str):
    print("")
    print("BŁĄD:")
    print("")
    if err_name == 'pln':
        print("PLN nie jest walutą OBCĄ :)")
        print("Kurs PLN do PLN zawsze wynosi 1:1")
    if err_name == 'response':
        print("Wprowadzona data jest weekendem (bank nie punlikuje wtedy notowań)")
        print("lub podano datę przed 2002r (tak starych kursów nie ma w archiwum API NBP)")
    if err_name == 'date':
        print("Błędny format daty!")
        print("Kursy nie zostaną obliczone :(")
    sys.exit(11)


def print_summary(currency:float,date:str):
    print ()
    print ("Waluta  :", currency) 
    print ("Data    :", date)
    print("-----")
    print("Łączę z API NBP...")
    print("-----")


def preprocess_response(response :Response) -> float:
    """extracts rate values from the response"""

    if response.ok:
        response_json = response.json()
        rate = response_json['rates'][0]['mid']
    else:
        print_error('response')
        sys.exit(13)
    return rate
        

def get_data_nbp_api(currency:float, date:str) -> Response:
    """Gets information about historical exchange rates from the Polish national bank's API"""

    currency=currency.upper()
    date_str = str(date)
    date = date_str[:10]
    print_summary(currency,date)
    url = f"http://api.nbp.pl/api/exchangerates/rates/A/{currency}/{date}"
    response = requests.get(url)
    return response        


def print_raport(rate :float, currency :str, date:datetime):
    print("Wynik :")
    print("Kurs waluty", currency.upper(), "z dnia ", date, "wynosi:", rate, "PLN")


def main():
    print_intro()
    currency = get_currency()
    unparsed_date = get_date()
    date = parse_date(unparsed_date)
    if currency.lower() == 'pln':
        print_error('pln')
    response = get_data_nbp_api(currency,date)
    rate = preprocess_response(response)
    print_raport(rate,currency,date)


if __name__ == '__main__':
    main()