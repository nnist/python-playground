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
        if filename.endswith('.txt'):
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
    options = {}
    options['length_min'] = 6
    options['length_max'] = 8
    options['double'] = False
    options['adjecent'] = False
    options['dict_file'] = 'nederlands3.txt'
    options['allowed_chars'] = 'qwertiopasdfgjkl'
    options['number'] = 12

    options_form = OptionsForm()

    if options_form.min_length.data == '' or options_form.min_length.data is None:
        options_form.min_length.data = options['length_min']
    else:
        options['length_min'] = int(options_form.min_length.data)

    if options_form.max_length.data == '' or options_form.max_length.data is None:
        options_form.max_length.data = options['length_max']
    else:
        options['length_max'] = int(options_form.max_length.data)

    if options_form.allowed_chars.data == '' or options_form.allowed_chars.data is None:
        options_form.allowed_chars.data = options['allowed_chars']
    else:
        options['allowed_chars'] = options_form.allowed_chars.data

    options['double'] = options_form.double.data
    options['adjecent'] = options_form.adjecent.data

    if options_form.wordlist.data == '' or options_form.wordlist.data is None:
        options_form.wordlist.data = options['dict_file']
    else:
        options['dict_file'] = options_form.wordlist.data

    generator = PassphraseGenerator(options)
    results = generator.generate()

    # Format and display words
    words = ''
    for word in results:
        words += word + '<br>'
    words = Markup(words)

    return render_template('index.html', title="Passphrase tool", words=words,
                           options_form=options_form)
