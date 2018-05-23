"""Show the web pages."""

from os import listdir
from flask import render_template, Markup
from app import app
from passphrase_tool import PassphraseGenerator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.fields.html5 import IntegerField
from wtforms.validators import DataRequired

class OptionsForm(FlaskForm):
    """Create fields for the options form."""
    min_length = IntegerField('Min length', validators=[DataRequired()])
    max_length = IntegerField('Max length', validators=[DataRequired()])
    allowed_chars = StringField('Allowed chars', validators=[DataRequired()])
    double = BooleanField('Double')
    adjecent = BooleanField('Adjecent')
    refresh = SubmitField('Refresh')

    # Get wordlists and populate dropdown menu
    wordlists = []
    for filename in listdir():
        if filename.endswith(".txt"):
            wordlists.append(filename)

    choices = []
    for wordlist in wordlists:
        choices.append((wordlist, wordlist))

    wordlist = SelectField('Wordlist', choices=choices, default=wordlists[1],
                           validators=[DataRequired()], coerce=str)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    """Show the index page."""
    length_min = 6
    length_max = 8
    double = False
    adjecent = False
    dict_file = "nederlands3.txt"
    allowed_chars = "qwertiopasdfgjkl"
    number = 12

    options_form = OptionsForm()

    if options_form.min_length.data == '' or options_form.min_length.data is None:
        options_form.min_length.data = length_min
    else:
        length_min = int(options_form.min_length.data)

    if options_form.max_length.data == '' or options_form.max_length.data is None:
        options_form.max_length.data = length_max
    else:
        length_max = int(options_form.max_length.data)

    if options_form.allowed_chars.data == '' or options_form.allowed_chars.data is None:
        options_form.allowed_chars.data = allowed_chars
    else:
        allowed_chars = options_form.allowed_chars.data

    double = options_form.double.data
    adjecent = options_form.adjecent.data

    if options_form.wordlist.data == '' or options_form.wordlist.data is None:
        options_form.wordlist.data = dict_file
    else:
        dict_file = options_form.wordlist.data

    generator = PassphraseGenerator(length_min, length_max, double, adjecent,
                                    allowed_chars, dict_file, number)
    results = generator.generate()

    # Format and display words
    words = ""
    for word in results:
        words += word + "<br>"
    words = Markup(words)

    return render_template('index.html', title='Passphrase tool', words=words,
                           options_form=options_form)
