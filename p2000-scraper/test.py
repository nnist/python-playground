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
def test_scraper_scrape_page():
    scraper = Scraper(3, 0, 1)
    results = scraper.scrape_page("http://www.p2000-online.net/p2000.php?\
                                     Pagina=0&AutoRefresh=uit")
    assert results != []

    # Ensure all scraped fields are valid
    for result in results:
        assert result['date_time'] is not None
        assert result['calltype'] is not None
        assert result['region'] is not None or \
            (result['calltype'] == 'KNRM' and result['region'] is None)
        priority = result['priority']
        assert priority is None or priority[0] in "ABP"
        postcode = result['postcode']
        assert postcode is None or re.findall(r'\d{4}[A-Z]{2}', postcode) != []
        assert result['details'] is not None
        #capcodes = result['capcodes']

@pytest.mark.timeout(10)
def test_scraper():
    scraper = Scraper(1, 0, 1)
    scraper.scrape()
    assert True
