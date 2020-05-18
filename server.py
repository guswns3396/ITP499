from flask import Flask, render_template, request, redirect, url_for
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import mysql.connector
import requests
import math
import hashlib

# create flask object
app = Flask(__name__)
# create session dictionary for session variables
session = {}

# load csv data & pre-process data
DF = pd.read_csv("data/covid_19_data.csv")
DF = DF[["ObservationDate","Country/Region","Confirmed"]]
DF = DF.groupby(["ObservationDate","Country/Region"]).sum().reset_index()
filter = DF["Country/Region"] == "US"
DF.where(filter, inplace=True)
DF = DF[["ObservationDate","Country/Region","Confirmed"]]
DF = DF.dropna()
DF = DF.reset_index()
DF = DF[["ObservationDate","Confirmed"]]
# from 3/22/20
# print(DF)
num_rows = DF["ObservationDate"].count()
DF = DF.iloc[60:num_rows]
# print(DF)

# visualize data
plt.figure()
plt.scatter([i for i in range(0,len(DF["ObservationDate"]))],DF["Confirmed"],s=0.1)
# plt.show()
# linear regression best fit

X = np.array([i-60 for i in range(60,num_rows)])
y = DF["Confirmed"]
y = y.to_numpy()
# print(X.shape)
# print(y.shape)

reg = LinearRegression().fit(X.reshape(-1,1),y)
# visualize fit
plt.plot(X,reg.predict(X.reshape(-1,1)))
# plt.show()

# connect to dbs
USER = "root"
PW = input("Input password for DB: ")
HOST = "localhost"
DB = "users_db"
try:
    cnx = mysql.connector.connect(user=USER, password=PW, host=HOST, database=DB)
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    exit()

@app.route("/")
def index():
    print(session)
    if "username" in session:
        return redirect(url_for("menu"))
    return render_template("index.html", session=session)

@app.route("/error")
def error():
    return render_template("error.html",session=session)

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signup_confirmation", methods=["POST"])
def signup_confirmation():
    # try inserting to database
    attributes = "user_name, user_password, user_email, user_fname, user_lname"
    sql = (
        "INSERT INTO users (" + attributes + ") "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    pw = hashlib.md5(request.form["user_password"].encode())
    data = (
        request.form["user_name"],
        pw.hexdigest(),
        request.form["user_email"],
        request.form["user_fname"],
        request.form["user_lname"]
    )
    try:
        cursor.execute(sql,data)
    except mysql.connector.Error as err:
        print(err)
        return redirect(url_for("error"))
    else:
        print("sql success")
    cnx.commit()
    session["username"] = request.form["user_name"]
    return redirect(url_for("menu"))

@app.route("/login", methods=["POST"])
def login():
    # try retrieving result from DB
    sql = ("SELECT * FROM users WHERE user_name = %s")
    data = (request.form["user_name"],)
    try:
        cursor.execute(sql,data)
    except mysql.connector.Error as err:
        print(err)
        return redirect(url_for("error"))
    else:
        print("sql success")
    results = cursor.fetchall()
    pw = hashlib.md5(request.form["user_pass"].encode())
    if results and (results[0][1] == pw.hexdigest()):
        session["username"] = results[0][0]
        return redirect(url_for("menu"))
    else:
        return render_template("login_error.html", session=session)

@app.route("/logout")
def logout():
    session.pop("username")
    return redirect(url_for("index"))

@app.route("/menu")
def menu():
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template("menu.html", session=session)

@app.route("/find")
def find():
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template("find.html", session=session)

@app.route("/find_result")
def find_result():
    if "username" not in session:
        return redirect(url_for("index"))
    # get ip address of request using ip-api
    ip = requests.get('https://ipapi.co/ip/').text
    print(ip)
    # make request to ip-api
    r = requests.get("http://ip-api.com/json/" + ip)
    print(r.text)
    data = r.json()
    if data["country"] != "United States":
        render_template("find_error.html", session=session)
    # make request to covid-19 api
    lat0 = float(data["lat"])
    lon0 = float(data["lon"])
    endpoint = "https://api.covid19api.com/country/united-states/status/confirmed?"
    startdate = str(datetime.date.today() - datetime.timedelta(days=7))
    enddate = str(datetime.date.today())
    time = "T00:00:00Z"
    startdate += time
    enddate += time
    query = endpoint + "from=" + startdate + "&to=" + enddate
    print(query)
    r = requests.get(query)
    data = r.json()
    print(data)
    # calculate range & count
    try:
        radius = float(request.args["radius"])
    except:
        return render_template("radius_error.html", session=session)
    else:
        count = 0
        R = 6371
        for result in data:
            lat1 = float(result["Lat"])
            lon1 = float(result["Lon"])
            x = R*(lat1-lat0)*(math.pi/180)*math.cos(math.radians(lon0))
            y = R*(lon1-lon0)*math.pi/180
            if x**2 + y**2 <= radius**2:
                count += 1
    return render_template("find_result.html",session=session,count=count,radius=radius)

@app.route("/predict")
def predict():
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template("predict.html", session=session)

@app.route("/predict_result", methods=["POST"])
def predict_result():
    if "username" not in session:
        return redirect(url_for("index"))
    try:
        date1 = datetime.datetime.strptime(request.form["date"],"%Y-%m-%d").date()
    except:
        return render_template("predict_error.html", session=session)
    else:
        date0 = datetime.date(2020,3,22)
        delta = date1 - date0
        delta = np.array([delta.days])
        print(delta)
        pred = reg.predict(delta.reshape(-1,1))
        print(pred, y[delta], pred-y[delta])
        return render_template("predict_result.html", session=session, pred=int(pred[0]), date=date1)

if __name__ == '__main__':
    app.run(debug = True)

cursor.close()
cnx.close()