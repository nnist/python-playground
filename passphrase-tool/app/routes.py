"""Show the web pages."""
# TODO Dockerize
# TODO Add short useful info about passphrases, with sources
# TODO Checkboxes for verbs, nouns, etc.
# TODO Add reset button to form
# TODO Present passphrase words in a better way

from flask import render_template
from app import app
from passphrase_tool import PassphraseGenerator
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
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

    min_length_data = options_form.min_length.data
    if min_length_data == '' or min_length_data is None:
        options_form.min_length.data = length_min
    else:
        length_min = int(min_length_data)

    max_length_data = options_form.max_length.data
    if max_length_data == '' or max_length_data is None:
        options_form.max_length.data = length_max
    else:
        length_max = int(max_length_data)

    allowed_chars_data = options_form.allowed_chars.data
    if allowed_chars_data == '' or allowed_chars_data is None:
        options_form.allowed_chars.data = allowed_chars
    else:
        allowed_chars = allowed_chars_data

    double = options_form.double.data
    adjecent = options_form.adjecent.data

    if not options_form.validate_on_submit():
        print('error: form not valid')
        # TODO Properly handle this

    generator = PassphraseGenerator(length_min, length_max, double, adjecent,
                                    allowed_chars, dict_file, number)
    results = generator.generate()
    words = {'words': str(results)}

    return render_template('index.html', title='Passphrase tool', words=words,
                           options_form=options_form)
