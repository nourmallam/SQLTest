from flask import Flask

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home(var):
    # data = request.form
    # data = str(data.get(key='url'))
    # if type(data) == str and len(data) > 1:
    #     driver.get(data)
    return f"Hello {var}!"

if __name__ == "__main__":
    app.run(debug=True)
