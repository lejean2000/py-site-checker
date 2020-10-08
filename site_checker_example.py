"""Module to check website changes
"""
from WebSite import WebSite


SITES = [
    'http://www.bolyaiverseny.hu/matek/feladat_regi.htm',

    'http://www.matematickaolympiada.cz/cs/olympiada-pro-zakladni-skoly/70-rocnik-20-21'
]

PICKLE_FOLDER = 'sites'

for url in SITES:
    site = WebSite(url, PICKLE_FOLDER)
    site.retrieve()
    site.check_for_changes()
