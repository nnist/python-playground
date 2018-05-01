# TODO Checkboxes for options
# TODO Button for generating passphrases
# TODO Passphrase output/display
# TODO Textbox for allowed characters
# TODO Passphrase information (tips, tricks, sources)
# TODO Dockerize

from flask import render_template
from app import app
from passphrase_tool import *

@app.route('/')
@app.route('/index')
def index():
    length_min = 12
    length_max = 12
    double = False
    adjecent = False
    dict_file = "nederlands3.txt"
    allowed_chars = "qwertiopasdfgjkl"
    number = 12
    
    generator = PassphraseGenerator(length_min, length_max, double, adjecent, allowed_chars, dict_file, number)
    results = generator.generate()
    words = {'words': str(results)}
    return render_template('index.html', title='Passphrase tool', words=words)
