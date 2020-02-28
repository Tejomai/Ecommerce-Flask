from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, session
from models import *
from wtforms import Form,validators
from forms import AddForm, LoginForm
from flask_login import logout_user, login_required, UserMixin

products_blueprint = Blueprint('products_route', __name__)

@products_blueprint.route('/logout')  # User Logout
@login_required
def logout():
    form = LoginForm(request.form)
    logout_user()
    return render_template('login.html', form=form)

@products_blueprint.route('/all_products/<string:mail>') # Displays all products to  users
@login_required
def all_products(mail):
    data = Products.query.all()
    return render_template('display_products.html', data=data, mail=mail, title="Products")
        

@products_blueprint.route('/my_prods/<string:mail>') # Displays only users products  
@login_required
def my_products(mail):
    user = Users.query.filter_by(user_mail = mail).one()
    data = Products.query.filter(Products.ref_user.any(user_mail = mail)).all()
    return render_template("product_options.html", data=data, mail=mail)

@products_blueprint.route('/add_prod/<string:mail>', methods=['GET', 'POST'])  # Adds product
@login_required
def add(mail):
    form = AddForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Users.query.filter_by(user_mail = mail).first()
        prod=Products(product_name=form.product_name.data, product_cost=form.product_cost.data, product_desc=form.product_desc.data)
        user.products.append(prod)
        db.session.commit()
        flash('Successfully added a product !')
        return redirect(url_for('products_route.my_products', mail=mail)) 
    return render_template('add_product.html', form = form, data=mail)

@products_blueprint.route('/delete/<string:mail>/<string:prod_name>', methods = ['GET']) # Deletes User product
@login_required
def delete(mail,prod_name):
    prod = Products.query.filter_by(product_name = prod_name).first()
    user = Users.query.filter_by(user_mail = mail).one()
    user.products.remove(prod)
    db.session.commit()
    flash("Record Has Been Deleted Successfully")
    return redirect(url_for('products_route.my_products', mail=mail))

@products_blueprint.route('/edit/<string:mail>/<string:prod_name>', methods =['GET']) #Edit User Product
@login_required
def edit(mail, prod_name):
    user = Users.query.filter_by(user_mail = mail).one()
    data = Products.query.filter(Products.ref_user.any(user_mail = mail)).filter_by(product_name=prod_name).first()
    return render_template('edit_form.html', data=data, mail=mail)
  
@products_blueprint.route('/update/<string:mail>/<string:prod_name>', methods =['GET','POST'])
@login_required
def update(mail,prod_name):
    if request.method == 'POST':
        p_name = request.form['product_name']
        p_cost = request.form['product_cost']
        p_desc = request.form.get("product_desc")
        prod = Products.query.filter_by(product_name = prod_name).first()
        user = Users.query.filter_by(user_mail = mail).one()
        user.products.remove(prod)
        db.session.delete(prod)
        db.session.commit()
        user = Users.query.filter_by(user_mail = mail).first()
        prod=Products(product_name=p_name, product_cost=p_cost, product_desc=p_desc)
        user.products.append(prod)
        db.session.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('products_route.my_products', mail=mail))
