from passphrase_tool import *

def test_number_of_words():
    generator = PassphraseGenerator(length_min=9, length_max=9, number=12)
    result = generator.generate()
    assert len(result) == 12
