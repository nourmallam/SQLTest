from flask import Blueprint, render_template, request
from selenium import webdriver

driver = webdriver.Edge()

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    # data = request.form
    # data = str(data.get(key='url'))
    # if type(data) == str and len(data) > 1:
    #     driver.get(data)
    return render_template("home.html")
