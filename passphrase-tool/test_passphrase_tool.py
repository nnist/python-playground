"""Test the passphrase tool and the web interface."""
from passphrase_tool import PassphraseGenerator
from app import app
import pytest

@pytest.fixture
def client():
    """Create a client for testing the web interface."""
    app.config['TESTING'] = True
    test_client = app.test_client()
    return test_client

def test_number_of_words():
    """Test the number of words."""
    generator = PassphraseGenerator(length_min=9, length_max=9, number=12)
    result = generator.generate()
    assert len(result) == 12

def test_minimum_length():
    """Test the minimum length of the words."""
    generator = PassphraseGenerator(length_min=7, length_max=12, number=500)
    results = generator.generate()
    for result in results:
        assert len(result) >= 7

def test_maximum_length():
    """Test the maximum length of the words."""
    generator = PassphraseGenerator(length_min=7, length_max=12, number=500)
    results = generator.generate()
    for result in results:
        assert len(result) <= 12

def test_invalid_input():
    """Test for invalid input."""
    generator = PassphraseGenerator(length_min=7, length_max=6, number=500)
    results = generator.generate()
    assert results == ["Error: Invalid input"]
    generator = PassphraseGenerator(length_min=7, length_max=8, number=500,
                                    dict_file="potato")
    results = generator.generate()
    assert results == ["Error: Dict file does not exist"]

def test_webserver_running(client):
    """Test to see if the webserver is running."""
    result = client.get('/')
    assert result.data != b'<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">\n<title>404 Not Found</title>\n<h1>Not Found</h1>\n<p>The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.</p>\n'
