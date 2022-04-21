from flask import Flask, request, render_template
import json
import requests
import mysql.connector
from db_conn import db_connection

application = Flask(__name__)


mydb = db_connection()
cur = mydb.cursor()

@application.route("/")
def index():
	return render_template("index.html")

@application.route("/monitor")
def monitor():
	return render_template("monitor.html")

tmp_time = 0
@application.route("/data") # Real time
def getdata():
	global tmp_time
	if tmp_time > 0 :
		sql = "select ctime,driverID,Speed from drivingRecord where ctime >%s" %(tmp_time)
	else:
		sql = "select ctime,driverID,Speed from drivingRecord"

	cur.execute(sql)
	datas = []
	for i in cur.fetchall():
		datas.append([i[0], i[1]])

	if len(datas) > 0 :
		tmp_time = datas[-1][0]

	return json.dumps(datas)

@application.route("/summary")
def summary():
	response_API = requests.get('https://www.askpython.com/')
	print(response_API.status_code)
	print(response_API)
	theResult = response_API
	return render_template("summary.html", results = theResult)


if __name__ == "__main__":
	application.run(port=5000,debug=True)