from TXTparser import getSummary, getSummaryByDay
from flask import Flask, request, render_template, Response
import json
from db_conn import db_connection
from dotenv import load_dotenv
from pypika import MySQLQuery, Table, Field

load_dotenv()

application = Flask(__name__)


mydb = db_connection()


@application.route("/")
def index():
    return render_template("index.html")


@application.route("/monitor")
def monitor():
    return render_template("monitor2.html")


# Real time
@application.route("/data")
@application.route("/data/all/<time_since>") 
@application.route("/data/all/<time_since>/<time_until>") 
@application.route("/data/<driver>")
@application.route("/data/<driver>/<time_since>")
@application.route("/data/<driver>/<time_since>/<time_until>")
def getdata(time_since = None, time_until = None, driver = None):
    global tmp_time
    record = Table('drivingRecord')
    q = MySQLQuery.from_(record).select(record.ctime, record.driverID, record.Speed, record.isRapidlySpeedup, record.isRapidlySlowdown, record.isOverspeed, record.isOverspeedFinished)
    if time_since:
        q = q.where(record.ctime > time_since)
    if time_until:
        q = q.where(record.ctime < time_until)
    if driver:
        q = q.where(record.driverID == driver)
    try:
        cur = mydb.cursor()
        cur.execute(q.get_sql())
        data = cur.fetchall()
        return json.dumps(data)
    except:
        return "Internal Server Error", 500


@application.route("/summary")
def summary():
    summary = getSummary()
    summary_by_date = getSummaryByDay()
    return render_template("summary.html", summary=summary, summary_by_date=summary_by_date)


if __name__ == "__main__":
    application.run(port=5000, debug=True)
