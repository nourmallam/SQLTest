from flask import Flask, request, render_template, redirect
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        url = request.form["nm"]
        if url[0:3] == "www":
            return redirect("https://" + url)
        elif url[0:8] == "https://":
            return redirect(url)
        else:
            return redirect("https://www." + url)
    return render_template("index.html")


@app.errorhandler(401)
def page_not_found(error):
    return render_template("error.html")


if __name__ == "__main__":
    app.run()
