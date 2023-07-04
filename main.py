from flask import Flask, request, render_template
import time
from pprint import pprint
from zapv2 import ZAPv2

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        url = request.form["nm"]
        if url[0:3] == "www":
            url_string = "https://" + url
        elif url[0:8] == "https://":
            url_string = url
        else:
            url_string = "https://www." + url

        target = "https://localhost"

        zap = ZAPv2(proxies={'http': target+":8090", 'https': target+":8090"})

        target = target + ":8080"

        print('Accessing target %s' % target)
        zap.urlopen(target)

        print('Traditional Spidering target %s' % target)
        zap.spider.scan(target)
        time.sleep(5)
        while int(zap.spider.status()) < 100:
            time.sleep(5)
            print('Spider progress %: ' + zap.spider.status())
            time.sleep(5)
        print('Spider completed')

        print('Scanning target %s' % target)
        zap.ascan.scan(target)
        time.sleep(5)
        while int(zap.ascan.status()) < 100:
            time.sleep(5)
            print('Ascan progress %: ' + zap.ascan.status())
            time.sleep(5)
        print('Ascan completed')

        # Report the results
        print('Hosts: ' + ', '.join(zap.core.hosts))
        print('Alerts: ')
        # prints all alerts. can be commented
        pprint(zap.core.alerts())
        # HTML Report
        with open('report.html', 'w') as f:
            f.write(zap.core.htmlreport(apikey='q3bb8vid3divcqe81g4f041f7p'))
        # XML Report
        with open('report.xml', 'w') as f:
            f.write(zap.core.xmlreport(apikey='q3bb8vid3divcqe81g4f041f7p'))

        zap.core.shutdown()
    return render_template("index.html")


if __name__ == "__main__":
    app.run(port="8000")