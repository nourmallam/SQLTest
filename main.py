from flask import Flask, request, url_for, render_template, redirect
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        url = request.form["nm"]
        return redirect(url)
    return render_template("index.html")


if __name__ == "__main__":
    app.run()
