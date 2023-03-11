from category_product_list_Leroy_Merlin import make_html_elements, replace_endline

import requests
from lxml.html import HtmlElement 

def test_make_html_elements():
    xpath = '//*[@id="product-listing"]/div[2]/a/h3'
    url = 'https://www.leroymerlin.pl/materialy-budowlane/materialy-budowlane-stan-surowy/cegly-klinkierowe,a1555.html'
    response = requests.get(url)
    got = make_html_elements(response,xpath)[0]
    assert type(got) == HtmlElement

def test_replace_endline():
    text = "coś\ncoś"
    got = replace_endline(text)
    expected = "coś coś"
    assert got == expected

