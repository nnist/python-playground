from passphrase_tool import *
import urllib.request

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

def test_webserver_running():
    contents = urllib.request.urlopen("http://127.0.0.1:5000").read()
    assert contents is not None
