"""
Script is taking URL address as argument.
Returns list of text fields of elements specified by xpath as a one-by-one list in text console.
URL can be easly copied from web browser.

Usage: Lista_produktow_z_kategorii_Leroy_Merlin.py url_to_category

"""

import click
from lxml import html
import requests


def print_intro():
    print()
    print("Lista elementów znajdująca się na stronie o wskazanym URL:")
    print("")


def make_html_elements(response, xpath):
    html_ = html.fromstring(response.text)
    elements = html_.xpath(xpath)
    return elements


@click.command()
@click.argument("url")
def create_elements_from_arguments(url):
    """ Takes URL address and xpath, returns wanted html elements specified by xpath"""

    XPATH = '//*[@id="product-listing"]/div/a/h3'
    response = requests.get(url)
    elements = make_html_elements(response,XPATH)
    return elements


def replace_endline(content):
    text = content.replace("\n", " ")
    return text


def print_list(elements):
    for element in elements:
        line = element.text_content().lstrip()
        line = replace_endline(line)
        print(line)


def main():
    print_intro()
    elements = create_elements_from_arguments(standalone_mode=False)
    print_list(elements)


if __name__ == "__main__":
    main()