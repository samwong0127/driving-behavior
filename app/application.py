from flask import Flask, request, render_template
import json
import mysql.connector
from db_conn import db_connection

application = Flask(__name__)


mydb = db_connection()
cur = mydb.cursor()

@application.route("/")
def index():
 return render_template("monitor.html")

tmp_time = 0

@application.route("/data")
def getdata():
	global tmp_time
	if tmp_time > 0 :
		sql = "select ctime,num from Monitor where ctime >%s" %(tmp_time)
	else:
		sql = "select ctime,num from Monitor"

	cur.execute(sql)
	datas = []
	for i in cur.fetchall():
		datas.append([i[0], i[1]])

	if len(datas) > 0 :
		tmp_time = datas[-1][0]

	return json.dumps(datas)


if __name__ == "__main__":
	application.run(port=5000,debug=True)