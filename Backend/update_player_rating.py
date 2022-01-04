import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor
import json
from datetime import datetime, timedelta
import os, sys
sys.path.append(os.getcwd())
import app_configuration as appConf    #Input File for providing DB details, table name, common string formats #Importing Constant variables file
import statuswho
import retcommon_status



def ratingsConvert_bowler(y_pred):
    y_pred=int(y_pred)
    if (y_pred==1):
        new_prediction="Low performer"
    elif (y_pred==2):
        new_prediction="Above low performer"
    elif (y_pred==3):
        new_prediction="Below average performer"
    elif (y_pred==4):
        new_prediction="Average performer"
    elif (y_pred==5):
        new_prediction="Above average performer"
    elif (y_pred==6):
        new_prediction="Good performer"
    elif (y_pred==7):
        new_prediction="Excellent performer"
    elif (y_pred==8):
        new_prediction="Best performer"
    else:
        new_prediction='no score'
    return new_prediction



class staticVar:
    connection = ""
    cursor = ""
    
def getDbConnection():
    result=-1
    status="default"
    status_who=""
    try:
        #DB Details fetched from the Configuration file
        staticVar.connection = psycopg2.connect(user = appConf.registrationDBConfig["user"],
                                        password = appConf.registrationDBConfig["password"],
                                        host = appConf.registrationDBConfig["host"],
                                        port = appConf.registrationDBConfig["port"],
                                        database = appConf.registrationDBConfig["database"])
        staticVar.cursor = staticVar.connection.cursor()
        status="success"
        status_who=statuswho.DB_CONNECTION_SUCCESS
        return retcommon_status.createJSONResponse(status,status_who,str(result))
    except (Exception, psycopg2.Error) as error :
        status="error"
        status_who=statuswho.DB_CONNECTION_FAILED
        return retcommon_status.createJSONResponse(status,status_who,str(result))
       
def isTableExist(tableName):
    result=-1
    status="default"
    status_who=""
    try:
        getDbConnection()
        table_exist_query = "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name ='"+tableName+"');"
        staticVar.cursor.execute(table_exist_query) # Should be logged
        if(staticVar.cursor.fetchone()[0]):
            status="success"
            status_who=statuswho.TABLE_EXIST
            return True
        else:
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
            return False
    except (Exception, psycopg2.DatabaseError) as error :
            status="error"
            status_who=statuswho.DATABASE_ERROR
            return retcommon_status.createJSONResponse(status,status_who,str(result))

def updatePredictBatsmanRating(tableName,name,toporder,middleorder,hitter):
    result=-1
    status="default"
    status_who=""
    try:
        if(isTableExist(tableName)):
            status="success"
            if not name is None:
                staticVar.cursor.execute(" UPDATE "+tableName+" SET toporder_rating ='"+toporder+"', midorder_rating ='"+middleorder+"', finisher_rating='"+hitter+"' WHERE player_name ='"+name+"';")

            staticVar.connection.commit()
            result = "Rating Updated Successfully."
            status_who=statuswho.UPDATE_TABLE_SUCCESS
            return retcommon_status.createJSONResponse(status,status_who,str(result))
        else:
            status="error"
            status_who=statuswho.UPDATE_TABLE_FAILURE
            return retcommon_status.createJSONResponse(status,status_who,str(result))
    except (Exception, psycopg2.DatabaseError) as error :
            status="error"
            status_who=statuswho.DATABASE_ERROR
            return retcommon_status.createJSONResponse(status,status_who,str(result))
    
    finally:
        closeConnection()


def predictBatsmanRating(tableBatsman,playerrole,role,minprice,maxprice):
    results=-1
    result = -1
    status="default"
    status_who=""
    batsmanPrediction=""
    try:
       if (isTableExist(tableBatsman) == False):
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
            return retcommon_status.createJSONResponse(status,status_who,str(result))

       #staticVar.cursor =  staticVar.connection.cursor(cursor_factory=RealDictCursor)
       if role == 'none':
            if playerrole == 'Top-Order-Batsman':
                fetch_query = "SELECT player_name,country,cap_status,baseprice,toporder_rating,description FROM "+tableBatsman+" INNER JOIN tbl_batsmanrating ON "+tableBatsman+".toporder_rating=tbl_batsmanrating.id  WHERE player_role='"+playerrole+"' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by toporder_rating desc, baseprice asc;"
                #"SELECT carregistrationno,vehicletype FROM "+tablevehicle+" INNER JOIN "+tableuser+ " ON "+tablevehicle+".uid="+tableuser+".uid WHERE email='"+email+"' ;"
                print("***",fetch_query)
                staticVar.cursor.execute(fetch_query)
                batsmanPrediction = staticVar.cursor.fetchall()
                results = []
                name=""
                basePrice=""
                predictedRating=""
                country=""
                capStatus=""
                position=playerrole
                description=""
                for row in batsmanPrediction:
                    name = str(row[0])
                    country=str(row[1])
                    capStatus=str(row[2])
                    basePrice = str(row[3])
                    predictedRating = str(row[4])
                    description = str(row[5])
                    results.append({"battingPosition": playerrole,"name": name, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating, "description":description}) 

            elif playerrole == 'Middle-Order-Batsman':
                fetch_query = "SELECT player_name,country,cap_status,baseprice,midorder_rating,description FROM "+tableBatsman+" INNER JOIN tbl_batsmanrating ON "+tableBatsman+".midorder_rating=tbl_batsmanrating.id  WHERE player_role='"+playerrole+"' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by midorder_rating desc, baseprice asc;"
                print("***",fetch_query)
                staticVar.cursor.execute(fetch_query)
                batsmanPrediction = staticVar.cursor.fetchall()
                results = []
                name=""
                baseprice=""
                predictedRating=""
                country=""
                capStatus=""
                position=playerrole
                description = ""
                for row in batsmanPrediction:
                    name = str(row[0])
                    country=str(row[1])
                    capStatus=str(row[2])
                    basePrice = str(row[3])
                    predictedRating = str(row[4])
                    description = str(row[5])
                
                    results.append({"battingPosition": playerrole,"name": name, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating, "description": description}) 
            else:
                fetch_query = "SELECT player_name,country,cap_status,baseprice,finisher_rating,description FROM "+tableBatsman+" INNER JOIN tbl_batsmanrating ON "+tableBatsman+".finisher_rating=tbl_batsmanrating.id  WHERE player_role='"+playerrole+"' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by finisher_rating desc, baseprice asc ;"
                print("***",fetch_query)
                staticVar.cursor.execute(fetch_query)
                batsmanPrediction = staticVar.cursor.fetchall()
                results = []
                name=""
                baseprice=""
                predictedRating=""
                country=""
                capStatus=""
                position=playerrole
                description=""
                for row in batsmanPrediction:
                    name = str(row[0])
                    country=str(row[1])
                    capStatus=str(row[2])
                    basePrice = str(row[3])
                    predictedRating = str(row[4])
                    description=str(row[5])
                    results.append({"battingPosition": playerrole,"name": name, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating, "description":description})

            staticVar.connection.commit()
            status="success"
            status_who=statuswho.FETCH_ALL_SUCCESS
            return retcommon_status.createJSONResponse(status,status_who,results)

       if role == 'Wicket-Keeper':
            if playerrole == 'Top-Order-Batsman':
                fetch_query = "SELECT player_name,country,cap_status,baseprice,toporder_rating,description FROM "+tableBatsman+" INNER JOIN tbl_batsmanrating ON "+tableBatsman+".toporder_rating=tbl_batsmanrating.id  WHERE player_role='"+playerrole+"' AND flag = '1' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by toporder_rating desc, baseprice asc;"
                              #"SELECT player_name,country,cap_status,baseprice,toporder_rating,description FROM "+tableBatsman+" INNER JOIN tbl_batsmanrating ON "+tableBatsman+".toporder_rating=tbl_batsmanrating.id  WHERE player_role='"+playerrole+"' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by toporder_rating desc, baseprice asc;"
                print("***",fetch_query)
                staticVar.cursor.execute(fetch_query)
                staticVar.connection.commit()
                playerData = staticVar.cursor.fetchall()
                results = []
                name=""
                basePrice=""
                predictedRating=""
                country=""
                capStatus=""
                count = 0
                for row in playerData:
                    name = str(row[0])
                    country=str(row[1])
                    capStatus=str(row[2])
                    basePrice = str(row[3])
                    predictedRating = str(row[4])
                    description = str(row[5])
                    results.append({"role": role, "name": name, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating,"battingPosition": playerrole, "description": description})

            if playerrole == 'Middle-Order-Batsman':
                fetch_query = "SELECT player_name,country,cap_status,baseprice,midorder_rating,description FROM "+tableBatsman+" INNER JOIN tbl_batsmanrating ON "+tableBatsman+".midorder_rating=tbl_batsmanrating.id  WHERE player_role='"+playerrole+"' AND flag = '1' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by midorder_rating desc, baseprice asc;"
                print("***",fetch_query)
                staticVar.cursor.execute(fetch_query)
                staticVar.connection.commit()
                playerData = staticVar.cursor.fetchall()
                results = []
                name=""
                basePrice=""
                predictedRating=""
                country=""
                capStatus=""
                count = 0
                for row in playerData:
                    name = str(row[0])
                    country=str(row[1])
                    capStatus=str(row[2])
                    basePrice = str(row[3])
                    predictedRating = str(row[4])
                    description = str(row[5])
                    results.append({"role": role,"name": name, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating,"battingPosition": playerrole,"description": description})
              
            else:
                fetch_query = "SELECT player_name,country,cap_status,baseprice,finisher_rating,description FROM "+tableBatsman+" INNER JOIN tbl_batsmanrating ON "+tableBatsman+".finisher_rating=tbl_batsmanrating.id  WHERE player_role='"+playerrole+"' AND flag = '1' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by finisher_rating desc, baseprice asc;"
                print("***",fetch_query)
                staticVar.cursor.execute(fetch_query)
                staticVar.connection.commit()
                playerData = staticVar.cursor.fetchall()
                results = []
                name=""
                basePrice=""
                predictedRating=""
                country=""
                capStatus=""
                description = ""
                count = 0
                for row in playerData:
                    name = str(row[0])
                    country=str(row[1])
                    capStatus=str(row[2])
                    basePrice = str(row[3])
                    predictedRating = str(row[4])
                    description= str(row[5])
                    results.append({"role": role,"name": name, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating,"battingPosition": playerrole, "description": description})

            staticVar.connection.commit()
            status="success"
            status_who=statuswho.FETCH_ALL_SUCCESS
            return retcommon_status.createJSONResponse(status,status_who,results)

       if role == 'All-Rounder':
            if playerrole == 'Top-Order-Batsman':
                fetch_query = "SELECT player_name,country,cap_status,baseprice,toporder_rating,description FROM "+tableBatsman+" INNER JOIN tbl_batsmanrating ON "+tableBatsman+".toporder_rating=tbl_batsmanrating.id  WHERE player_role='"+playerrole+"' AND flag = '2' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by toporder_rating desc, baseprice asc;"
                              #"SELECT player_name,country,cap_status,baseprice,toporder_rating,description FROM "+tableBatsman+" INNER JOIN tbl_batsmanrating ON "+tableBatsman+".toporder_rating=tbl_batsmanrating.id  WHERE player_role='"+playerrole+"' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by toporder_rating desc, baseprice asc;"
                print("***",fetch_query)
                staticVar.cursor.execute(fetch_query)
                staticVar.connection.commit()
                playerData = staticVar.cursor.fetchall()
                results = []
                name=""
                basePrice=""
                predictedRating=""
                country=""
                capStatus=""
                count = 0
                for row in playerData:
                    name = str(row[0])
                    country=str(row[1])
                    capStatus=str(row[2])
                    basePrice = str(row[3])
                    predictedRating = str(row[4])
                    description = str(row[5])
                    results.append({"role": role, "name": name, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating,"battingPosition": playerrole, "description": description})

            if playerrole == 'Middle-Order-Batsman':
                fetch_query = "SELECT player_name,country,cap_status,baseprice,midorder_rating,description FROM "+tableBatsman+" INNER JOIN tbl_batsmanrating ON "+tableBatsman+".midorder_rating=tbl_batsmanrating.id  WHERE player_role='"+playerrole+"' AND flag = '2' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by midorder_rating desc, baseprice asc;"
                print("***",fetch_query)
                staticVar.cursor.execute(fetch_query)
                staticVar.connection.commit()
                playerData = staticVar.cursor.fetchall()
                results = []
                name=""
                basePrice=""
                predictedRating=""
                country=""
                capStatus=""
                count = 0
                for row in playerData:
                    name = str(row[0])
                    country=str(row[1])
                    capStatus=str(row[2])
                    basePrice = str(row[3])
                    predictedRating = str(row[4])
                    description = str(row[5])
                    results.append({"role": role,"name": name, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating,"battingPosition": playerrole,"description": description})
              
            else:
                fetch_query = "SELECT player_name,country,cap_status,baseprice,finisher_rating,description FROM "+tableBatsman+" INNER JOIN tbl_batsmanrating ON "+tableBatsman+".finisher_rating=tbl_batsmanrating.id  WHERE player_role='"+playerrole+"' AND flag = '2' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by finisher_rating desc, baseprice asc;"
                print("***",fetch_query)
                staticVar.cursor.execute(fetch_query)
                staticVar.connection.commit()
                playerData = staticVar.cursor.fetchall()
                results = []
                name=""
                basePrice=""
                predictedRating=""
                country=""
                capStatus=""
                description = ""
                count = 0
                for row in playerData:
                    name = str(row[0])
                    country=str(row[1])
                    capStatus=str(row[2])
                    basePrice = str(row[3])
                    predictedRating = str(row[4])
                    description= str(row[5])
                    results.append({"role": role,"name": name, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating,"battingPosition": playerrole, "description": description})

            staticVar.connection.commit()
            status="success"
            status_who=statuswho.FETCH_ALL_SUCCESS
            return retcommon_status.createJSONResponse(status,status_who,results)    
    finally:
        closeConnection()

def predictWicketKeeperRating(tableBatsman,role,minprice,maxprice):
    results=-1
    result = -1
    status="default"
    status_who=""
    playerData=""
    try:
       if (isTableExist(tableBatsman) == False):
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
            return retcommon_status.createJSONResponse(status,status_who,str(result))

       #staticVar.cursor =  staticVar.connection.cursor(cursor_factory=RealDictCursor)
       if role == 'wicketKeeper':
            fetch_query = "SELECT player_name,country,cap_status,baseprice,player_role,midorder_rating FROM "+tableBatsman+" WHERE flag = '1' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by baseprice asc;"
            print("*********",fetch_query)
            staticVar.cursor.execute(fetch_query)
            staticVar.connection.commit()
            playerData = staticVar.cursor.fetchall()
            results = []
            name=""
            basePrice=""
            predictedRating=""
            country=""
            capStatus=""
            count = 0
            for row in playerData:
                   name = str(row[0])
                   country=str(row[1])
                   capStatus=str(row[2])
                   basePrice = str(row[3])
                   predictedRating = str(row[4])
                   player_role = str(row[5])
                   results.append({"role": role, "shortlistedPlayers":{"name": name, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating,"player_role": player_role}})
            staticVar.connection.commit()
            status="success"
            status_who=statuswho.FETCH_ALL_SUCCESS
            return retcommon_status.createJSONResponse(status,status_who,results)
       else:
        staticVar.connection.commit()
        status="success"
        status_who=statuswho.FETCH_ALL_FAILURE
        return retcommon_status.createJSONResponse(status,status_who,results)
    except (Exception, psycopg2.DatabaseError) as error :
            status="error"
            status_who=statuswho.DATABASE_ERROR
            return retcommon_status.createJSONResponse(status,status_who,str(result))
    
    finally:
        closeConnection()

def predictBowlerRating(tableBowler,role,bowlingstyle,minprice,maxprice):
    results=-1
    result = -1
    status="default"
    status_who=""
    playerData=""
    try:
       if (isTableExist(tableBowler) == False):
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
            return retcommon_status.createJSONResponse(status,status_who,str(result))

       #staticVar.cursor =  staticVar.connection.cursor(cursor_factory=RealDictCursor)
       if role == 'Bowler':
            fetch_query = "SELECT player_name,player_role,country,cap_status,baseprice,rating FROM "+tableBowler+" WHERE player_role='"+bowlingstyle+"' AND flag ='0' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by rating desc, baseprice asc;"
            print("***",fetch_query)
            staticVar.cursor.execute(fetch_query)
            staticVar.connection.commit()
            playerData = staticVar.cursor.fetchall()
            results = []
            name=""
            bowlingStyle=""
            basePrice=""
            predictedRating=""
            country=""
            capStatus=""
            count = 0
            for row in playerData:
                name = str(row[0])
                bowlingStyle= str(row[1])
                country=str(row[2])
                capStatus=str(row[3])
                basePrice = str(row[4])
                predictedRating = str(row[5])
                ratingDescription=ratingsConvert_bowler(predictedRating)
                results.append({ "name": name, "bowlingStyle": bowlingStyle, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating,"description":ratingDescription}) 

            staticVar.connection.commit()
            status="success"
            status_who=statuswho.FETCH_ALL_SUCCESS
            return retcommon_status.createJSONResponse(status,status_who,results)
            #results =  uservehicleData 
            #return results

       if role == 'All-Rounder':
            fetch_query = "SELECT player_name,player_role,country,cap_status,baseprice,rating FROM "+tableBowler+" WHERE player_role='"+bowlingstyle+"' AND flag ='1' AND baseprice >='"+minprice+"' AND baseprice <= '"+maxprice+"' order by rating desc, baseprice asc;"
            print("***",fetch_query)
            staticVar.cursor.execute(fetch_query)
            staticVar.connection.commit()
            playerData = staticVar.cursor.fetchall()
            results = []
            name=""
            bowlingStyle=""
            basePrice=""
            predictedRating=""
            country=""
            capStatus=""
            count = 0
            for row in playerData:
                name = str(row[0])
                bowlingStyle= str(row[1])
                country=str(row[2])
                capStatus=str(row[3])
                basePrice = str(row[4])
                predictedRating = str(row[5])
                ratingDescription=ratingsConvert_bowler(predictedRating)
                results.append({ "name": name, "bowlingStyle": bowlingStyle, "country": country, "capStatus": capStatus, "basePrice": basePrice,"predictedRating": predictedRating,"description":ratingDescription}) 

            staticVar.connection.commit()
            status="success"
            status_who=statuswho.FETCH_ALL_SUCCESS
            return retcommon_status.createJSONResponse(status,status_who,results)


    except (Exception, psycopg2.DatabaseError) as error :
            status="error"
            status_who=statuswho.DATABASE_ERROR
            return retcommon_status.createJSONResponse(status,status_who,str(result))
    
    finally:
        closeConnection()

def checkBatsmanPerformance(tableBatsman,name,innings,average,strikerate,fifties,hundreds,fours,sixes,ducks,totalruns,ballsfaced,notouts):
    result=-1
    status="default"
    status_who=""
    try:
        if (isTableExist(tableBatsman)==False):
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
            return retcommon_status.createJSONResponse(status,status_who,str(result))

        insert_query = "INSERT INTO "+tableBatsman+"(name,innings,average,strikerate,fifties,hundreds,fours,sixes,ducks,totalruns,ballsfaced,notouts) VALUES('"+name+"','"+innings+"','"+average+"','"+strikerate+"','"+fifties+"','"+hundreds+"','"+fours+"','"+sixes+"','"+ducks+"','"+totalruns+"','"+ballsfaced+"','"+notouts+"') ;"
        print("*********",insert_query)
        staticVar.cursor.execute(insert_query)
        staticVar.connection.commit()
        count = staticVar.cursor.rowcount
        #result = "New Vehicle Registration Number "+carregistrationno+" added successfully."
        result = {"PlayerDataMsg": "Batsman Data added successfully"}
        status="success"
        status_who=statuswho.INSERT_BATPLAYER_SUCCESS
        return retcommon_status.createJSONResponse(status,status_who,result)
        
    except (Exception, psycopg2.DatabaseError) as error :
            status="error"
            status_who=statuswho.DATABASE_ERROR
            return retcommon_status.createJSONResponse(status,status_who,str(result))
    
    finally:
        closeConnection()


def closeConnection():
    result=-1
    status="default"
    status_who=""
    try:
        if(staticVar.DBConnectionData["isDBConnected"]):
            staticVar.cursor.close()
            staticVar.connection.close()
            staticVar.DBConnectionData["isDBConnected"] = False
            status="success"
            status_who=statuswho.DB_CLOSE_CONNECTION_SUCCESS
            return retcommon_status.createJSONResponse(status,status_who,str(result))
    except (Exception, psycopg2.Error) as error :
        status="error"
        status_who=statuswho.DB_CLOSE_CONNECTION_FAILURE
        return retcommon_status.createJSONResponse(status,status_who,str(result))


def getCountPlayerPerRating(tablebatsman,tableBowler,role,price):
    results=-1
    result = -1
    status="default"
    status_who=""
    playerData=""
    try:
       if (isTableExist(tableBowler) == False):
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
            return retcommon_status.createJSONResponse(status,status_who,str(result))
       if (isTableExist(tablebatsman) == False):
            status="error"
            status_who=statuswho.TABLE_DOESNOT_EXIST
            return retcommon_status.createJSONResponse(status,status_who,str(result))

       #staticVar.cursor =  staticVar.connection.cursor(cursor_factory=RealDictCursor)
       if role == 'Batsman':
            fetch_query_top1 =  "select toporder_rating,count(toporder_rating) from tbl_batsmanauction where player_role = 'Top-Order-Batsman' AND toporder_rating ='1' AND baseprice <= '"+price+"' group by toporder_rating;"
            print("***",fetch_query_top1)
            staticVar.cursor.execute(fetch_query_top1)
            staticVar.connection.commit()
            playerData1 = staticVar.cursor.fetchall()
            results = []
            rating1Counttop =""
            for row in playerData1:
                if row == None:
                    rating1Counttop = 0
                else:
                    rating1Counttop = str(row[1])
            #return rating1Counttop            

            fetch_query_top2 =  "select toporder_rating,count(toporder_rating) from tbl_batsmanauction where player_role = 'Top-Order-Batsman' AND toporder_rating ='2' AND baseprice <= '"+price+"' group by toporder_rating;"
            print("***",fetch_query_top2)
            staticVar.cursor.execute(fetch_query_top2)
            staticVar.connection.commit()
            playerData2= staticVar.cursor.fetchall()
            rating2Counttop=""
            for row in playerData2:
                if row == None:
                    rating2Counttop = 0
                else:
                    rating2Counttop = str(row[1])
            #return rating2Counttop

            fetch_query_top3=  "select toporder_rating,count(toporder_rating) from tbl_batsmanauction where player_role = 'Top-Order-Batsman' AND toporder_rating ='3' AND baseprice <= '"+price+"' group by toporder_rating;"
            print("***",fetch_query_top3)
            staticVar.cursor.execute(fetch_query_top3)
            staticVar.connection.commit()
            playerData3= staticVar.cursor.fetchall()
            rating3Counttop=""
            for row in playerData3:
                if row == None:
                    rating3Counttop = 0
                else:
                    rating3Counttop = str(row[1])
            #return rating3Counttop

            fetch_query_top4=  "select toporder_rating,count(toporder_rating) from tbl_batsmanauction where player_role = 'Top-Order-Batsman' AND toporder_rating ='4' AND baseprice <= '"+price+"' group by toporder_rating;"
            print("***",fetch_query_top4)
            staticVar.cursor.execute(fetch_query_top4)
            staticVar.connection.commit()
            playerData4= staticVar.cursor.fetchall()
            rating4Counttop=""
            for row in playerData4:
                if row == None:
                    rating4Counttop = 0
                else:
                    rating4Counttop = str(row[1])
 
            fetch_query_top5=  "select toporder_rating,count(toporder_rating) from tbl_batsmanauction where player_role = 'Top-Order-Batsman' AND toporder_rating ='5' AND baseprice <= '"+price+"' group by toporder_rating;"
            print("***",fetch_query_top5)
            staticVar.cursor.execute(fetch_query_top5)
            staticVar.connection.commit()
            playerData5= staticVar.cursor.fetchall()
            rating5Counttop=""
            for row in playerData5:
                if row == None:
                    rating5Counttop = 0
                else:
                    rating5Counttop = str(row[1])

            fetch_query_mid1 =  "select midorder_rating,count(midorder_rating) from tbl_batsmanauction where player_role = 'Middle-Order-Batsman' AND midorder_rating ='1' AND baseprice <= '"+price+"' group by midorder_rating;"
            print("***",fetch_query_mid1)
            staticVar.cursor.execute(fetch_query_mid1)
            staticVar.connection.commit()
            playerData1mid = staticVar.cursor.fetchall()
            results = []
            rating1Countmid =""
            for row in playerData1mid:
                if row == None:
                    rating1Countmid = 0
                else:
                    rating1Countmid = str(row[1])
            #return rating1Counttop            

            fetch_query_mid2 =  "select midorder_rating,count(midorder_rating) from tbl_batsmanauction where player_role = 'Middle-Order-Batsman' AND midorder_rating ='2' AND baseprice <= '"+price+"' group by midorder_rating;"
            print("***",fetch_query_mid2)
            staticVar.cursor.execute(fetch_query_mid2)
            staticVar.connection.commit()
            playerData2mid= staticVar.cursor.fetchall()
            rating2Countmid=""
            for row in playerData2mid:
                if row == None:
                    rating2Countmid = 0
                else:
                    rating2Countmid = str(row[1])
            #return rating2Counttop

            fetch_query_mid3=  "select midorder_rating,count(midorder_rating) from tbl_batsmanauction where player_role = 'Middle-Order-Batsman' AND midorder_rating ='3' AND baseprice <= '"+price+"' group by midorder_rating;"
            print("***",fetch_query_mid3)
            staticVar.cursor.execute(fetch_query_mid3)
            staticVar.connection.commit()
            playerData3mid= staticVar.cursor.fetchall()
            rating3Countmid=""
            for row in playerData3mid:
                if row == None:
                    rating3Countmid = 0
                else:
                    rating3Countmid = str(row[1])
            #return rating3Counttop

            fetch_query_mid4=  "select midorder_rating,count(midorder_rating) from tbl_batsmanauction where player_role = 'Middle-Order-Batsman' AND midorder_rating ='4' AND baseprice <= '"+price+"' group by midorder_rating;"
            print("***",fetch_query_mid4)
            staticVar.cursor.execute(fetch_query_mid4)
            staticVar.connection.commit()
            playerData4mid= staticVar.cursor.fetchall()
            rating4Countmid=""
            for row in playerData4mid:
                if row == None:
                    rating4Countmid = 0
                else:
                    rating4Countmid = str(row[1])
 
            fetch_query_mid5=  "select midorder_rating,count(midorder_rating) from tbl_batsmanauction where player_role = 'Middle-Order-Batsman' AND midorder_rating ='5' AND baseprice <= '"+price+"' group by midorder_rating;"
            print("***",fetch_query_mid5)
            staticVar.cursor.execute(fetch_query_mid5)
            staticVar.connection.commit()
            playerData5mid= staticVar.cursor.fetchall()
            rating5Countmid=""
            for row in playerData5mid:
                if row == None:
                    rating5Countmid = 0
                else:
                    rating5Countmid = str(row[1])

            fetch_query_fin1 =  "select finisher_rating,count(finisher_rating) from tbl_batsmanauction where player_role = 'Finisher-Batsman' AND finisher_rating ='1' AND baseprice <= '"+price+"' group by finisher_rating;"
            print("***",fetch_query_fin1)
            staticVar.cursor.execute(fetch_query_fin1)
            staticVar.connection.commit()
            playerData1fin = staticVar.cursor.fetchall()
            results = []
            rating1Countfin =""
            for row in playerData1fin:
                if row == None:
                    rating1Countfin = 0
                else:
                    rating1Countfin = str(row[1])
            #return rating1Counttop            

            fetch_query_fin2 =  "select finisher_rating,count(finisher_rating) from tbl_batsmanauction where player_role = 'Finisher-Batsman' AND finisher_rating ='2' AND baseprice <= '"+price+"' group by finisher_rating;"
            print("***",fetch_query_fin2)
            staticVar.cursor.execute(fetch_query_fin2)
            staticVar.connection.commit()
            playerData2fin= staticVar.cursor.fetchall()
            rating2Countfin=""
            for row in playerData2fin:
                if row == None:
                    rating2Countfin = 0
                else:
                    rating2Countfin = str(row[1])
            #return rating2Counttop

            fetch_query_fin3=  "select finisher_rating,count(finisher_rating) from tbl_batsmanauction where player_role = 'Finisher-Batsman' AND finisher_rating ='3' AND baseprice <= '"+price+"' group by finisher_rating;"
            print("***",fetch_query_fin3)
            staticVar.cursor.execute(fetch_query_fin3)
            staticVar.connection.commit()
            playerData3fin= staticVar.cursor.fetchall()
            rating3Countfin=""
            for row in playerData3fin:
                if row == None:
                    rating3Countfin = 0
                else:
                    rating3Countfin = str(row[1])
            #return rating3Counttop

            fetch_query_fin4=  "select finisher_rating,count(finisher_rating) from tbl_batsmanauction where player_role = 'Finisher-Batsman' AND finisher_rating ='4' AND baseprice <= '"+price+"' group by finisher_rating;"
            print("***",fetch_query_fin4)
            staticVar.cursor.execute(fetch_query_fin4)
            staticVar.connection.commit()
            playerData4fin= staticVar.cursor.fetchall()
            rating4Countfin=""
            for row in playerData4fin:
                if row == None:
                    rating4Countfin = 0
                else:
                    rating4Countfin = str(row[1])
 
            fetch_query_fin5=  "select finisher_rating,count(finisher_rating) from tbl_batsmanauction where player_role = 'Finisher-Batsman' AND finisher_rating ='5' AND baseprice <= '"+price+"' group by finisher_rating;"
            print("***",fetch_query_fin5)
            staticVar.cursor.execute(fetch_query_fin5)
            staticVar.connection.commit()
            playerData5fin= staticVar.cursor.fetchall()
            rating5Countfin=""
            for row in playerData5fin:
                if row == None:
                    rating5Countfin = 0
                else:
                    rating5Countfin = str(row[1])
    
            top_order_response = { "rating1Count":rating1Counttop,"rating2Count":rating2Counttop,"rating3Count":rating3Counttop,"rating4Count":rating4Counttop,"rating5Count":rating5Counttop}           
            mid_order_response = { "rating1Count":rating1Countmid,"rating2Count":rating2Countmid,"rating3Count":rating3Countmid,"rating4Count":rating4Countmid,"rating5Count":rating5Countmid}    
            fin_order_response = { "rating1Count":rating1Countfin,"rating2Count":rating2Countfin,"rating3Count":rating3Countfin,"rating4Count":rating4Countfin,"rating5Count":rating5Countfin}    

            final_response= {'Role':'Batsman', 'topOrderBatsman':top_order_response, 'midOrderBatsman':mid_order_response,'finisherBatsman':fin_order_response}
            staticVar.connection.commit()
            status="success"
            status_who=statuswho.FETCH_ALL_SUCCESS
            return retcommon_status.createJSONResponse(status,status_who,final_response)

       if role == 'Bowler':
            fetch_query_fast8 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Fast-Bowler' AND rating ='8' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_fast8)
            staticVar.cursor.execute(fetch_query_fast8)
            staticVar.connection.commit()
            playerData8fast= staticVar.cursor.fetchall()
            rating8Countfas=""
            for row in playerData8fast:
                if row == None:
                    rating8Countfas = 0
                else:
                    rating8Countfas = str(row[1])
    
            fetch_query_fast7 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Fast-Bowler' AND rating ='7' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_fast7)
            staticVar.cursor.execute(fetch_query_fast7)
            staticVar.connection.commit()
            playerData7fast= staticVar.cursor.fetchall()
            rating7Countfas=""
            for row in playerData7fast:
                if row == None:
                    rating7Countfas = 0
                else:
                    rating7Countfas = str(row[1])

            fetch_query_fast6 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Fast-Bowler' AND rating ='6' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_fast6)
            staticVar.cursor.execute(fetch_query_fast6)
            staticVar.connection.commit()
            playerData6fast= staticVar.cursor.fetchall()
            rating6Countfas=""
            for row in playerData6fast:
                if row == None:
                    rating6Countfas = 0
                else:
                    rating6Countfas = str(row[1])

            fetch_query_fast5 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Fast-Bowler' AND rating ='5' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_fast5)
            staticVar.cursor.execute(fetch_query_fast5)
            staticVar.connection.commit()
            playerData5fast= staticVar.cursor.fetchall()
            rating5Countfas=""
            for row in playerData5fast:
                if row == None:
                    rating5Countfas = 0
                else:
                    rating5Countfas = str(row[1])

            fetch_query_fast4 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Fast-Bowler' AND rating ='4' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_fast4)
            staticVar.cursor.execute(fetch_query_fast4)
            staticVar.connection.commit()
            playerData4fast= staticVar.cursor.fetchall()
            rating4Countfas=""
            for row in playerData4fast:
                if row == None:
                    rating4Countfas = 0
                else:
                    rating4Countfas = str(row[1])

            fetch_query_fast3 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Fast-Bowler' AND rating ='3' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_fast3)
            staticVar.cursor.execute(fetch_query_fast3)
            staticVar.connection.commit()
            playerData3fast= staticVar.cursor.fetchall()
            rating3Countfas=""
            for row in playerData3fast:
                if row == None:
                    rating3Countfas = 0
                else:
                    rating3Countfas = str(row[1])

            fetch_query_fast2 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Fast-Bowler' AND rating ='2' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_fast2)
            staticVar.cursor.execute(fetch_query_fast2)
            staticVar.connection.commit()
            playerData2fast= staticVar.cursor.fetchall()
            rating2Countfas=""
            for row in playerData2fast:
                if row == None:
                    rating2Countfas = 0
                else:
                    rating2Countfas = str(row[1])

            fetch_query_fast1 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Fast-Bowler' AND rating ='1' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_fast1)
            staticVar.cursor.execute(fetch_query_fast1)
            staticVar.connection.commit()
            playerData1fast= staticVar.cursor.fetchall()
            rating1Countfas=""
            for row in playerData1fast:
                if row == None:
                    rating1Countfas = 0
                else:
                    rating1Countfas = str(row[1])

            fetch_query_spin8 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Spin-Bowler' AND rating ='8' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_spin8)
            staticVar.cursor.execute(fetch_query_spin8)
            staticVar.connection.commit()
            playerData8spin= staticVar.cursor.fetchall()
            rating8Countspin=""
            for row in playerData8spin:
                if row == None:
                    rating8Countspin = 0
                else:
                    rating8Countspin = str(row[1])
    
            fetch_query_spin7 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Spin-Bowler' AND rating ='7' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_spin7)
            staticVar.cursor.execute(fetch_query_spin7)
            staticVar.connection.commit()
            playerData7spin= staticVar.cursor.fetchall()
            rating7Countspin=""
            for row in playerData7spin:
                if row == None:
                    rating7Countspin = 0
                else:
                    rating7Countspin = str(row[1])

            fetch_query_spin6 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Spin-Bowler' AND rating ='6' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_spin6)
            staticVar.cursor.execute(fetch_query_spin6)
            staticVar.connection.commit()
            playerData6spin= staticVar.cursor.fetchall()
            rating6Countspin=""
            for row in playerData6spin:
                if row == None:
                    rating6Countspin = 0
                else:
                    rating6Countspin = str(row[1])

            fetch_query_spin5 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Spin-Bowler' AND rating ='5' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_spin5)
            staticVar.cursor.execute(fetch_query_spin5)
            staticVar.connection.commit()
            playerData5spin= staticVar.cursor.fetchall()
            rating5Countspin=""
            for row in playerData5spin:
                if row == None:
                    rating5Countspin = 0
                else:
                    rating5Countspin = str(row[1])

            fetch_query_spin4 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Spin-Bowler' AND rating ='4' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_spin4)
            staticVar.cursor.execute(fetch_query_spin4)
            staticVar.connection.commit()
            playerData4spin= staticVar.cursor.fetchall()
            rating4Countspin=""
            for row in playerData4spin:
                if row == None:
                    rating4Countspin = 0
                else:
                    rating4Countspin = str(row[1])

            fetch_query_spin3 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Spin-Bowler' AND rating ='3' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_spin3)
            staticVar.cursor.execute(fetch_query_spin3)
            staticVar.connection.commit()
            playerData3spin= staticVar.cursor.fetchall()
            rating3Countspin=""
            for row in playerData3spin:
                if row == None:
                    rating3Countspin = 0
                else:
                    rating3Countspin = str(row[1])

            fetch_query_spin2 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Spin-Bowler' AND rating ='2' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_spin2)
            staticVar.cursor.execute(fetch_query_spin2)
            staticVar.connection.commit()
            playerData2spin= staticVar.cursor.fetchall()
            rating2Countspin=""
            for row in playerData2spin:
                if row == None:
                    rating2Countspin = 0
                else:
                    rating2Countspin = str(row[1])

            fetch_query_spin1 = "SELECT rating,count(rating) from tbl_bowlingauction where player_role = 'Spin-Bowler' AND rating ='1' AND baseprice <= '"+price+"' group by rating;"
            print("***",fetch_query_spin1)
            staticVar.cursor.execute(fetch_query_spin1)
            staticVar.connection.commit()
            playerData1spin= staticVar.cursor.fetchall()
            rating1Countspin=""
            for row in playerData1spin:
                if row == None:
                    rating1Countspin = 0
                else:
                    rating1Countspin = str(row[1])

            spin_bowler_response = { "rating1Count":int(rating1Countspin),"rating2Count":int(rating2Countspin),"rating3Count":int(rating3Countspin),"rating4Count":int(rating4Countspin),"rating5Count":int(rating5Countspin),"rating6Count":int(rating6Countspin),"rating7Count":rating7Countspin,"rating8Count":int(rating8Countspin)}           
            fast_bowler_response = { "rating1Count":rating1Countfas,"rating2Count":rating2Countfas,"rating3Count":rating3Countfas,"rating4Count":rating4Countfas,"rating5Count":rating5Countfas,"rating6Count":rating6Countfas,"rating7Count":rating7Countfas,"rating8Count":rating8Countfas}           

            final_bowler_response= {'Role':'Bowler', 'Fast-Bowler':fast_bowler_response, 'Spin-Bowler':spin_bowler_response}
            staticVar.connection.commit()
            status="success"
            status_who=statuswho.FETCH_ALL_SUCCESS
            return retcommon_status.createJSONResponse(status,status_who,final_bowler_response)

    except (Exception, psycopg2.DatabaseError) as error :
            status="error"
            status_who=statuswho.DATABASE_ERROR
            return retcommon_status.createJSONResponse(status,status_who,str(result))
    
    finally:
        closeConnection()