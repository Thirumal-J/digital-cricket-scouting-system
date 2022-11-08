import math
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.model_selection import train_test_split
from imblearn.combine import SMOTETomek
import pandas as pd
from flask_cors import CORS
import update_player_rating as update
import app_configuration as appConf
from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
import sys
sys.path.append(os.getcwd())

app = Flask(__name__)
CORS(app)
api = Api(app)

db = SQLAlchemy(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


@app.route('/', methods=['GET'])
def home():
    return "<h1>Hello</p>"

#Initiating Database Connection
class DBConnection(Resource):
    def get(self):
        return update.getDbConnection()

#Predicting the batsman performance
class predictBatsman(Resource):
    def post(self):
        inputJson = request.get_json()
        battingPosition = inputJson["battingPosition"]
        role = inputJson["role"]
        minprice = inputJson["minPrice"]
        maxprice = inputJson["maxPrice"]
        return update.predictBatsmanRating(appConf.BatsmantableName, battingPosition, role, minprice, maxprice)

#Predicting the wicketkeeper performance
class predictWicketKeeper(Resource):
    def post(self):

        inputJson = request.get_json()
        battingPosition = inputJson["battingPosition"]
        minprice = inputJson["minPrice"]
        maxprice = inputJson["maxPrice"]
        return update.predictWicketKeeperRating(appConf.BatsmantableName, battingPosition, minprice, maxprice)

#Predicting the bowler performance
class predictBowler(Resource):
    def post(self):
        inputJson = request.get_json()
        role = inputJson["role"]
        bowlingstyle = inputJson["bowlingStyle"]
        minprice = inputJson["minPrice"]
        maxprice = inputJson["maxPrice"]
        print(inputJson)
        return update.predictBowlerRating(appConf.BowlerstableName, role, bowlingstyle, minprice, maxprice)

#Updating the batsman rating
class updatePredictBatsmanRating(Resource):
    def post(self):
        inputJson = request.get_json()
        name = inputJson["name"]
        toporder = inputJson["toporder"]
        middleorder = inputJson["middleorder"]
        hitter = inputJson["hitter"]
        return update.updatePredictBatsmanRating(appConf.BatsmantableName, name, toporder, middleorder, hitter)

#Checking the batsman performance
class CheckBatsmanPerformance(Resource):
    def get(self):
        inputJson = request.get_json()
        name = inputJson["name"]
        innings = inputJson["innings"]
        average = inputJson["average"]
        strikeRate = inputJson["strikeRate"]
        fifties = inputJson["fifties"]
        hundreds = inputJson["hundreds"]
        fours = inputJson["fours"]
        sixes = inputJson["sixes"]
        ducks = inputJson["ducks"]
        totalRuns = inputJson["totalRuns"]
        ballsFaced = inputJson["ballsFaced"]
        notOuts = inputJson["notOuts"]
        return update.checkBatsmanPerformance(appConf.CheckBatsmanPerformanceTableName, name, innings, average, strikeRate, fifties, hundreds, fours, sixes, ducks, totalRuns, ballsFaced, notOuts)

#Training the batsman model
@app.route("/trainbatsman")
def trainbatsman():
    count = 0
    for count in range(3):
        train_batsman = pd.read_csv('./Dataset/Train_Batsman.csv')
        train_batsman = train_batsman.dropna()
        train_batsman = train_batsman[train_batsman["Ave"] != "-"]
        train_batsman["Ave"] = train_batsman["Ave"].astype("float")
        if (count == 0):
            train_batsman["Performance"] = (0.026*train_batsman["Inn"])+(0.063*train_batsman["Runs"])+(0.23*train_batsman["Ave"])+(0.232*train_batsman["SR"])+(0.15*train_batsman["4s"])+(
                0.154*train_batsman["6s"])+(0.024*train_batsman["NO"])+(0.027*train_batsman["50"])+(0.023*train_batsman["100"])+(0.047*train_batsman["Balls"])-(0.023*train_batsman["0"])
        elif (count == 1):
            train_batsman["Performance"] = (0.021*train_batsman["Inn"])+(0.068*train_batsman["Runs"])+(0.23*train_batsman["Ave"])+(0.232*train_batsman["SR"])+(0.15*train_batsman["4s"])+(
                0.154*train_batsman["6s"])+(0.024*train_batsman["NO"])+(0.027*train_batsman["50"])+(0.023*train_batsman["100"])+(0.047*train_batsman["Balls"])-(0.023*train_batsman["0"])
        else:
            train_batsman["Performance"] = (0.03*train_batsman["Inn"])+(0.059*train_batsman["Runs"])+(0.23*train_batsman["Ave"])+(0.232*train_batsman["SR"])+(0.15*train_batsman["4s"])+(
                0.154*train_batsman["6s"])+(0.024*train_batsman["NO"])+(0.027*train_batsman["50"])+(0.023*train_batsman["100"])+(0.047*train_batsman["Balls"])-(0.023*train_batsman["0"])
        train_batsman["Performance"] = 10 * \
            (train_batsman["Performance"]/max(train_batsman["Performance"]))
        for index, row in train_batsman.iterrows():
            if train_batsman["Performance"][index] >= 7:
                train_batsman["Performance"][index] = "5"
            elif train_batsman["Performance"][index] >= 5.5 and train_batsman["Performance"][index] < 7:
                train_batsman["Performance"][index] = "4"
            elif train_batsman["Performance"][index] >= 3 and train_batsman["Performance"][index] < 5.5:
                train_batsman["Performance"][index] = "3"
            elif train_batsman["Performance"][index] >= 2 and train_batsman["Performance"][index] < 3:
                train_batsman["Performance"][index] = "2"
            else:
                train_batsman["Performance"][index] = "1"

        train_batsman['Performance'] = train_batsman['Performance'].astype(
            'int')
        train_batsman = train_batsman.iloc[:, 1:]
        target = train_batsman['Performance']
        train = train_batsman.drop(['Performance', 'HS', 'Mat'], axis=1)

        # Random Forest

        smk = SMOTETomek(random_state=42)
        train_new, target_new = smk.fit_resample(train, target)
        X_train, X_test, y_train, y_test = train_test_split(
            train_new, target_new, test_size=0.20, random_state=0)
        model = RandomForestClassifier(n_estimators=50)
        model.fit(X_train, y_train)

        if count == 0:
            joblib.dump(model, 'model_batsman_toporder.pkl')
        elif count == 1:
            joblib.dump(model, 'model_batsman_midorder.pkl')
        else:
            joblib.dump(model, 'model_batsman_finisher.pkl')
    return "Trained"

#Fetching the batsman ratings using the model
@app.route("/fetchRatings/batsman/<manualflag>", methods=['GET', 'POST'])
def fetchRatingsbatsman(manualflag):
    manualflag = int(manualflag)
    model_toporder = joblib.load('model_batsman_toporder.pkl')
    model_midorder = joblib.load('model_batsman_midorder.pkl')
    model_finisher = joblib.load('model_batsman_finisher.pkl')
    response = {
        "role": "batsman",
        "ratings":
            {
                "topOrder": {
                    "rating": "",
                    "Description": "",
                },
                "middleOrder": {
                    "rating": "",
                    "Description": "",
                },
                "finisher": {
                    "rating": "",
                    "Description": ""
                }
            }
    }
    if (manualflag == 0):
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()
        query = "select player_name,innings,notouts,totalruns,average,ballsfaced,strikerate,hundreds,fifties,ducks,fours,sixes from tbl_batsmanauction "
        cur.execute(query)
        datatable = cur.fetchall()
        for row in datatable:
            playerName = row[0]
            Inn = row[1]
            NO = row[2]
            Runs = row[3]
            Ave = row[4]
            Balls = row[5]
            SR = row[6]
            hundreds = row[7]
            fifties = row[8]
            ducks = row[9]
            fours = row[10]
            sixes = row[11]

            y_pred_toporder = model_toporder.predict(
                [[Inn, NO, Runs, Ave, Balls, SR, hundreds, fifties, ducks, fours, sixes]])
            y_pred_midorder = model_midorder.predict(
                [[Inn, NO, Runs, Ave, Balls, SR, hundreds, fifties, ducks, fours, sixes]])
            y_pred_finisher = model_finisher.predict(
                [[Inn, NO, Runs, Ave, Balls, SR, hundreds, fifties, ducks, fours, sixes]])

            y_pred_toporder = " ".join(str(x) for x in y_pred_toporder)
            y_pred_midorder = " ".join(str(x) for x in y_pred_midorder)
            y_pred_finisher = " ".join(str(x) for x in y_pred_finisher)

            sql = "update tbl_batsmanauction set toporder_rating=" + str(y_pred_toporder) + ", midorder_rating="+str(
                y_pred_midorder)+",finisher_rating="+(y_pred_finisher)+" where player_name='"+playerName+"'"
            cur.execute(sql)

        conn.commit()

    elif (manualflag == 1):
        Inn = request.json["innings"]
        NO = request.json["notOuts"]
        Runs = request.json["totalRuns"]
        Ave = request.json["average"]
        Balls = request.json["ballsFaced"]
        SR = request.json["strikeRate"]
        hundreds = request.json["hundreds"]
        fifties = request.json["fifties"]
        ducks = request.json["ducks"]
        fours = request.json["fours"]
        sixes = request.json["sixes"]

        y_pred_toporder = model_toporder.predict(
            [[Inn, NO, Runs, Ave, Balls, SR, hundreds, fifties, ducks, fours, sixes]])
        y_pred_midorder = model_midorder.predict(
            [[Inn, NO, Runs, Ave, Balls, SR, hundreds, fifties, ducks, fours, sixes]])
        y_pred_finisher = model_finisher.predict(
            [[Inn, NO, Runs, Ave, Balls, SR, hundreds, fifties, ducks, fours, sixes]])

        new_prediction_toporder = ratingsConvert_batsman(y_pred_toporder)
        ratingsConvert_batsman(y_pred_midorder)
        ratingsConvert_batsman(y_pred_finisher)
        y_pred_toporder = " ".join(str(x) for x in y_pred_toporder)
        y_pred_midorder = " ".join(str(x) for x in y_pred_midorder)
        y_pred_finisher = " ".join(str(x) for x in y_pred_finisher)
        response = {
            "role": "batsman",
            "ratings":
            {
                "topOrder": {
                    "rating": str(y_pred_toporder),
                    "Description": str(new_prediction_toporder),
                },
                "middleOrder": {
                    "rating": str(4),
                    "Description": str("Above Average Performer"),
                },
                "finisher": {
                    "rating": str(5),
                    "Description": str("Best Performer")
                }
            }
        }

    else:
        return "invalid flag input"
    print(response)
    return jsonify(response)

#Categorizing the batsman ratings
def ratingsConvert_batsman(y_pred):
    if (y_pred == 1):
        new_prediction = "Low performer"
    if (y_pred == 2):
        new_prediction = "Below average performer"
    if (y_pred == 3):
        new_prediction = "Average performer"
    if (y_pred == 4):
        new_prediction = "Above average performer"
    else:
        new_prediction = 'Best performer'
    return new_prediction

#Training the bowler model
@app.route("/trainbowler")
def trainbowler():
    train_bowler = pd.read_csv('./Dataset/Train_Bowling.csv')
    train_bowler = train_bowler.dropna()
    train_bowler["Performance"] = (0.041*train_bowler["Inn"])+(0.056*train_bowler["Overs"])+(0.364*train_bowler["Wkts"])-(
        0.318*train_bowler["Econ"])+(0.056*train_bowler["Mdns"])+(0.099*train_bowler["4w"])+(0.066*train_bowler["5w"])
    train_bowler["Performance"] = train_bowler["Performance"] + \
        abs(min(train_bowler.Performance))
    train_bowler["Performance"] = 10 * \
        (train_bowler["Performance"]/max(train_bowler["Performance"]))

    for index, row in train_bowler.iterrows():
        train_bowler["Performance"][index] = math.ceil(
            train_bowler["Performance"][index])
        if train_bowler["Performance"][index] >= 9:
            train_bowler["Performance"][index] = "9"

    train_bowler['Performance'] = train_bowler['Performance'].astype('int')
    train_bowler = train_bowler[train_bowler["Performance"] != 0]
    train_bowler = train_bowler.iloc[:, 1:]
    target = train_bowler['Performance']
    train = train_bowler.drop('Performance', axis=1).drop(
        ['Ave', 'SR', 'Runs', 'Mat'], axis=1)

    # Random Forest

    from imblearn.combine import SMOTETomek
    smk = SMOTETomek(random_state=42)
    train_new, target_new = smk.fit_resample(train, target)

    X_train, X_test, y_train, y_test = train_test_split(
        train_new, target_new, test_size=0.20, random_state=0)
    model = RandomForestClassifier(n_estimators=50)
    model.fit(X_train, y_train)
    joblib.dump(model, 'model_bowler.pkl')
    return "Trained"

#Fetching the bowler ratings using model
@app.route("/fetchRatings/bowler/<manualflag>", methods=['GET', 'POST'])
def fetchRatingsbowler(manualflag):
    manualflag = int(manualflag)
    model = joblib.load('model_bowler.pkl')
    response = {
        "role": "",
        "ratings": ''
    }

    if (manualflag == 0):
        conn = psycopg2.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
        cur = conn.cursor()
        query = "select player_name,innings,overs,wickets,economy,maidens,fourwickethaul,fivewickethaul from tbl_bowlingauction "
        cur.execute(query)
        datatable = cur.fetchall()
        for row in datatable:
            playerName = row[0]
            Inn = row[1]
            Overs = row[2]
            Wkts = row[3]
            Econ = row[4]
            Mdns = row[5]
            fourwickethaul = row[6]
            fivewickethaul = row[7]

            y_pred_bowler = model.predict(
                [[Inn, Overs, Wkts, Econ, Mdns, fourwickethaul, fivewickethaul]])

            y_pred_bowler = " ".join(str(x) for x in y_pred_bowler)

            sql = "update tbl_bowlingauction set rating=" + \
                str(y_pred_bowler) + " where player_name='"+playerName+"'"
            cur.execute(sql)

        conn.commit()
    elif (manualflag == 1):
        Inn = request.json["innings"]
        Overs = request.json["innings"]
        Wkts = request.json["innings"]
        Econ = request.json["innings"]
        Mdns = request.json["innings"]
        fourwickethaul = request.json["innings"]
        fivewickethaul = request.json["innings"]

        y_pred_bowler = model.predict(
            [[Inn, Overs, Wkts, Econ, Mdns, fourwickethaul, fivewickethaul]])
        y_pred_bowler = " ".join(str(x) for x in y_pred_bowler)

        new_prediction_bowler = ratingsConvert_bowler(y_pred_bowler)

        response = {
            "role": "bowler",
            "ratings": {
                "rating": y_pred_bowler,
                "Description": new_prediction_bowler
            }
        }
    else:
        return "invalid flag input"
    return jsonify(response)

#Categorizing the bowler ratings
def ratingsConvert_bowler(y_pred):
    y_pred = int(y_pred)
    if (y_pred == 1):
        new_prediction = "Low performer"
    elif (y_pred == 2):
        new_prediction = "Above low performer"
    elif (y_pred == 3):
        new_prediction = "Below average performer"
    elif (y_pred == 4):
        new_prediction = "Average performer"
    elif (y_pred == 5):
        new_prediction = "Above average performer"
    elif (y_pred == 6):
        new_prediction = "Good performer"
    elif (y_pred == 7):
        new_prediction = "Excellent performer"
    elif (y_pred == 8):
        new_prediction = "Best performer"
    else:
        new_prediction = 'no score'
    return new_prediction

#Updating the batsman details
@app.route("/updatedatabatsman")
def updatedatabatsman():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()
    query = "delete from tbl_batsmanauction "
    cur.execute(query)
    f_contents = open('input_batsman.csv', 'r')
    cur.copy_from(f_contents, "tbl_batsmanauction", columns=('player_name', 'country', 'cap_status',
                                                             'baseprice', 'innings', 'totalruns', 'ballsfaced', 'average', 'strikerate', 'fifties', 'hundreds', 'fours',
                                                             'sixes', 'notouts', 'player_role', 'flag'), sep=",")
    conn.commit()
    return "done"

#Updating the bowler details
@app.route("/updatedatabowler")
def updatedatabowler():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()
    f_contents = open('Data_bowlingauction.csv', 'r')
    cur.copy_from(f_contents, "tbl_bowlingauction", columns=('player_name',
                                                             'player_role', 'country', 'cap_status', 'baseprice', 'innings', 'overs', 'wickets', 'economy', 'maidens', 'fourwickethaul',
                                                             'fivewickethaul', 'flag'), sep=",")
    conn.commit()
    return "done"

#Fetching the baseprice of the players in auction
@app.route("/basepricegraph/<baseprice>")
def basepricegraph(baseprice):

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                            password=DB_PASS, host=DB_HOST)
    cur = conn.cursor()
    query = "select baseprice,count(*) from tbl_batsmanauction where baseprice<" + \
        baseprice+"group by baseprice order by baseprice"
    cur.execute(query)
    cur.fetchall()
    return jsonify(cur.fetchall())

#Categorizing the players based on rating
class countPlayerPerRating(Resource):
    def post(self):

        inputJson = request.get_json()
        role = inputJson["role"]
        price = inputJson["price"]
        return update.getCountPlayerPerRating(appConf.BatsmantableName, appConf.BowlerstableName, role, price)

#adding all the resources to the api
api.add_resource(DBConnection, "/getDbConnection")
api.add_resource(predictBatsman, "/predictBatsman")
api.add_resource(predictWicketKeeper, "/predictWicketKeeper")
api.add_resource(predictBowler, "/predictBowler")
api.add_resource(updatePredictBatsmanRating, "/updatePredictBatsmanRating")
api.add_resource(CheckBatsmanPerformance, "/CheckBatsmanPerformance")
api.add_resource(countPlayerPerRating, "/getCountPlayerPerRating")

if __name__ == '__main__':
    app.run(debug=True, port=8000)
