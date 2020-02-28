from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from models import *
from wtforms import Form,validators
from forms import SignupForm, LoginForm
from flask_login import login_required, logout_user, login_user, LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
index_blueprint = Blueprint('index', __name__)

@login_manager.user_loader
def load_user(user_id):
    user = Users.query.filter_by(user_id = user_id ).first()
    return user

@index_blueprint.route('/', methods=['GET', 'POST']) #Sign Up Page
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        pw_hash = flask_bcrypt.generate_password_hash(form.user_paswd.data)
        user = Users(user_name=form.user_name.data, user_mail=form.user_mail.data, user_paswd = pw_hash)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('index.login'))
    return render_template('signup.html', form=form, title="Sign Up")

@index_blueprint.route('/login', methods=['GET', 'POST']) #Login Page
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Users.query.filter_by(user_mail = form.user_mail.data).first()
        if user and flask_bcrypt.check_password_hash(user.user_paswd, form.user_paswd.data):
            login_user(user)
            session['user_mail'] = form.user_mail.data
            if(form.user_mail.data == 'admin@mail.com'):
                users = Users.query.all()
                return render_template('admin_page.html', data = users, title="Admin Page")
            else:
                data = Products.query.all()
                mail=form.user_mail.data
                return render_template('display_products.html', data=data, mail=mail, title="Products")
        
        else:
            flash("Login name or Password is wrong. If not an user Sign In.")
    return render_template('login.html', form=form, title="Login Page")
