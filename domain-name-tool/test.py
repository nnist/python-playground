"""Test the domain name tool."""
import pytest
from domaintool import DomainChecker
import subprocess

def test_get_domains():
    """Test the get_domains method."""
    domain_checker = DomainChecker(3, 4, 'io', delay=1.5)
    domains = domain_checker.get_domains()
    assert domains != []

def test_check_domain():
    """Test the check_domain method."""
    domain_checker = DomainChecker(3, 4, 'io', delay=1.5)
    assert domain_checker.check_domain('ado.be') == 'not_available'
    assert domain_checker.check_domain('jhgtyasjkhjdffd.be') == 'available'

def test_check_domains():
    """Test the check_domains method."""
    domain_checker = DomainChecker(13, 13, 'be', delay=0.1)
    domains = domain_checker.get_domains()
    domain_checker.check_domains(domains)
    assert True

def test_cli():
    """Test the cli."""
    process = subprocess.run(['python3 domaintool.py -h'],
                             shell=True,
                             timeout=10,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=True)
    output = process.stdout.split(b'\n')
    assert output[0] == b'usage: domaintool.py [-h] [-f FILE] ' +\
                        b'[-d DELAY] min max tld'

    process = subprocess.run(['python3 domaintool.py 13 13 be -d 0.1'],
                             shell=True,
                             timeout=10,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, check=True)
    output = process.stdout.split(b'\n')
    assert output[0] == b'Checking 7 domains...'
