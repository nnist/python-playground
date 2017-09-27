from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname':'sadcat'}
    posts = [
        {
            'author': {'nickname': 'johntato'},
            'body': 'today is good day'
        },
        {
            'author': {'nickname': 'susan'},
            'body': 'avengers r cool'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' % 
            (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
            title='Sign in',
            form=form,
            providers=app.config['OPENID_PROVIDERS'])
