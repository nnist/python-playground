from passphrase_tool import *
import urllib.request
from app import app
import pytest

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    return client

def test_number_of_words():
    generator = PassphraseGenerator(length_min=9, length_max=9, number=12)
    result = generator.generate()
    assert len(result) == 12

def test_minimum_length():
    generator = PassphraseGenerator(length_min=7, length_max=12, number=500)
    results = generator.generate()
    for result in results:
        assert len(result) >= 7

def test_maximum_length():
    generator = PassphraseGenerator(length_min=7, length_max=12, number=500)
    results = generator.generate()
    for result in results:
        assert len(result) <= 12

def test_invalid_input():
    generator = PassphraseGenerator(length_min=7, length_max=6, number=500)
    results = generator.generate()
    assert results == ["Error: Invalid input"]

def test_webserver_running(client):
    rv = client.get('/')
    assert rv.data != b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>\n'
