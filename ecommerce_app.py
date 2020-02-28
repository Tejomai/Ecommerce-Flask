from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import *

from views.index import index_blueprint
app.register_blueprint(index_blueprint)

from views.products_route import products_blueprint
app.register_blueprint(products_blueprint)

from views.admin_route import admin_blueprint
app.register_blueprint(admin_blueprint)

if __name__ == "__main__":
   app.run(debug=True)