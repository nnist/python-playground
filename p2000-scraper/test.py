"""Test the scraper."""
import subprocess
import re
import pytest
from scraper import Scraper

@pytest.mark.timeout(10)
def test_scraper_get_page():
    """Test the get_page method to make sure valid html is returned."""
    scraper = Scraper(1, 0, 1)
    html, status = scraper.get_page("http://www.p2000-online.net/p2000.php?\
                                     Pagina=0&AutoRefresh=uit")
    print(html)
    assert html is not None and status == 200

@pytest.mark.timeout(10)
def test_scraper_scrape_page():
    """Ensure all scraped fields contain valid information."""
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
    """Ensure the scraper runs at all."""
    scraper = Scraper(1, 0, 1)
    scraper.scrape()
    assert True

def test_scraper_cli():
    """Test the scraper cli."""
    process = subprocess.run(['python3 scraper.py -h'],
                             shell=True,
                             timeout=10,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=True)
    output = process.stdout.split(b'\n')
    assert output[0] == b'usage: scraper.py [-h] [-p PAGES] ' +\
                        b'[-o OFFSET] [-t THREADS]'

    process = subprocess.run(['python3 scraper.py -p 2 -o 0 -t 1'],
                             shell=True,
                             timeout=10,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=True)
    output = process.stdout.split(b'\n')
    assert output[0].startswith(b'Scraping ')
    assert output[-2].startswith(b'Done! Added ')

def test_stats_cli():
    """Test the stats cli."""
    process = subprocess.run(['python3 stats.py -h'],
                             shell=True,
                             timeout=10,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=True)
    output = process.stdout.split(b'\n')
    assert output[0] == b'usage: stats.py [-h] [-a] [-r] [-f] [--type] ' +\
                        b'[--region] [-t TIME]'

    #process = subprocess.run(['python3 stats.py'],
    #                         shell=True,
    #                         timeout=10,
    #                         stdout=subprocess.PIPE,
    #                         stderr=subprocess.PIPE, check=True)
    #output = process.stdout.split(b'\n')
    #assert output[0] == b'Nothing to show.'

    process = subprocess.run(['python3 stats.py -r'],
                             shell=True,
                             timeout=10,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=True)
    output = process.stdout.split(b'\n')
    assert output[1] == b'Most recent message'
    assert output[3] != b''

    process = subprocess.run(['python3 stats.py -f'],
                             shell=True,
                             timeout=10,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=True)
    output = process.stdout.split(b'\n')
    assert output[1] == b'First message'
    assert output[3] != b''

    process = subprocess.run(['python3 stats.py --type'],
                             shell=True,
                             timeout=10,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=True)
    output = process.stdout.split(b'\n')
    assert output[1] == b'Number of calls per type'
    assert output[3] != b''

    process = subprocess.run(['python3 stats.py --region'],
                             shell=True,
                             timeout=10,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=True)
    output = process.stdout.split(b'\n')
    assert output[1] == b'Number of messages per region'
    assert output[3] != b''

    process = subprocess.run(['python3 stats.py -t 31'],
                             shell=True,
                             timeout=10,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=True)
    output = process.stdout.split(b'\n')
    assert output[1].startswith(b'All messages of last 31 minutes')
    assert output[3] != b''
