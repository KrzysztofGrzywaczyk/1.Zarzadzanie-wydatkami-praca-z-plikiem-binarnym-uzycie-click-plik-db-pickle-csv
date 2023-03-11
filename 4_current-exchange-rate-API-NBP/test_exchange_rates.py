
from exchange_rates import get_data_nbp_api, parse_date, preprocess_response

import requests

def test_date_points():
    date = '02.03.2022'
    got = str(parse_date(date))
    expected = '2022-02-03 00:00:00'
    assert got == expected

def test_date_pauses():
    date = '25-10-2023'
    got = str(parse_date(date))
    expected = '2023-10-25 00:00:00'
    assert got == expected

def test_date_words():
    date = '20 may 2020'
    got = str(parse_date(date))
    expected = '2020-05-20 00:00:00'
    assert got == expected

def test_preprocessing_response():
    url = "http://api.nbp.pl/api/exchangerates/rates/A/EUR/2022-11-04"
    response = requests.get(url)
    got = preprocess_response(response)
    expected = 4.6898
    assert got == expected

def test_link_construction():
    currency = 'EUR'
    date = '2022-11-04 00:00'
    got = get_data_nbp_api(currency,date)
    assert got.ok == True
