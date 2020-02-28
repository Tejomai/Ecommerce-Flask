from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from models import *
from wtforms import Form,validators
from forms import LoginForm
from flask_login import logout_user, login_required, UserMixin

admin_blueprint = Blueprint('admin_route', __name__)

@admin_blueprint.route('/remove_user/<int:id>', methods=['GET', 'POST'])  # To remove a user by Admin 
@login_required
def remove_user(id):
    obj = Users.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    users = Users.query.all()
    return render_template("admin_page.html", data=users)

@admin_blueprint.route('/users') # Displays all users to admin
@login_required
def user():
    data = Users.query.all()
    return render_template("admin_products.html", data=data)

@admin_blueprint.route('/products') # Displays all products to admin
@login_required
def prods():
    products = Products.query.all()
    return render_template("admin_products.html", data=products)

@admin_blueprint.route('/del_prod/<int:id>', methods=['GET', 'POST'])  # To delete a product
@login_required
def delete_prod(id):
    obj = Products.query.get(id)
    db.session.delete(obj)
    db.session.commit()
    products = Products.query.all()
    return render_template("admin_products.html", data=products)

@admin_blueprint.route('/logout')  # Admin Logout
def logout():
    form = LoginForm(request.form)
    logout_user()
    return render_template('login.html', form=form)


