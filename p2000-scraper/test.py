import pytest
from scraper import *

@pytest.mark.timeout(10)
def test_scraper_get_page():
    scraper = Scraper(1, 0, 1)
    html, status = scraper.get_page("http://www.p2000-online.net/p2000.php?\
                                     Pagina=0&AutoRefresh=uit")
    print(html)
    assert html is not None and status is 200

@pytest.mark.timeout(10)
def test_scraper():
    scraper = Scraper(1, 0, 1)
    scraper.scrape()
    assert True
