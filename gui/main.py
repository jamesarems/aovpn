from flask import Flask, render_template, url_for
import json,os
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts='192.168.101.20')

esData = es.search(index='postoffice')

posts = esData['hits']['hits']


## Flask bind
app: Flask = Flask(__name__)


def readConf():
    with open('/etc/aovpn/aovpn-config.json') as json_file:
        data = json.load(json_file)
        return data

def test():
    appUpdate = "New Update available , 2.0 Spiderman"
    return appUpdate


def srvCheck(service):
    ## Check services
    if ( service == 'vpnserver'):
        srvStatus = os.popen('systemctl status openvpn@server | head -3 | grep running | cut -c 20-26').read(7)
        return srvStatus
    elif ( service == 'webserver'):
        srvStatus = os.popen('systemctl status httpd | head -3 | grep running | cut -c 20-26').read(7)
        return  srvStatus
    else:
        return 'no service'


## Flask Section
@app.route("/")
@app.route("/home")
def home():
    notes = test()
    config = readConf()
    vpnSrv = srvCheck('vpnserver')
    webSrv = srvCheck('webserver')
    realLog = os.popen('sudo tail -n 10 /var/log/openvpn.log').read()
    logs = realLog.splitlines()
    return render_template('home.html', notes=notes, len=len(logs), logs=logs, vpnserver=vpnSrv, webserver=webSrv, config=config)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/configuration")
def configuration():
    config = readConf()
    return render_template("config.html", config=config)


@app.route("/service")
def service():
    return render_template("services.html")


@app.route("/package")
def package():
    return render_template("package.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8080')