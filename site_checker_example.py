"""Module to check website changes
"""
from WebSite import WebSite


SITES = [
    'http://www.bolyaiverseny.hu/matek/feladat_regi.htm',

    'http://www.matematickaolympiada.cz/cs/olympiada-pro-zakladni-skoly/70-rocnik-20-21'
]

PICKLE_FOLDER = 'sites'

# Check all sites for updates
for url in SITES:
    site = WebSite(url, PICKLE_FOLDER)
    if site.retrieve():
        site.check_for_changes()

# compare last and second to last version of one site
url = 'http://www.bolyaiverseny.hu/matek/feladat_regi.htm'
site = WebSite(url, PICKLE_FOLDER)
site.diff(1, 0)
