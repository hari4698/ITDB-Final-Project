import psycopg2
import psycopg2.extras
import simplejson as json
from pymongo import MongoClient

# try:
# connection = psycopg2.connect(user = "plantadmin",
#                                 password = "theadminoftheplant",
#                                 host = "127.0.0.1",
#                                 port = "5432",
#                                 database = "powerplant")

# cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
# cursor.execute("SELECT statecode, statename FROM statecodetoname")
# records = cursor.fetchall()
# print(type(records))
# except (Exception, psycopg2.Error) as error :
#     print ("Error while connecting to PostgreSQL", error)
# finally:
#     #closing database connection.
#         if(connection):
#             cursor.close()
#             connection.close()
#             print("PostgreSQL connection is closed")
class PowerPlantData:

    def __init__(self):
    	self.conn = psycopg2.connect(user = "plantadmin",
                                password = "theadminoftheplant",
                                host = "127.0.0.1",
                                port = "5432",
                                database = "powerplant")
        #self.conn = psycopg2.connect(connection_string)

    def get_air_quality_info_by_state(self, statename):
        cursor1 = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)  
        query = "SELECT Good_Days, Max_NO2_days, Max_PM_days, Rate_of_NOx, Rate_of_PM FROM \
        (SELECT avg(averagegooddays) as Good_Days, \
         avg(maxno2days) as Max_NO2_days, avg(maxpmdays) as Max_PM_days, statename \
from airquality GROUP BY  airquality.statename) as airqualitystate \
 INNER JOIN \
(select avg(noxrate) as Rate_of_NOx, avg(pmrate) as Rate_of_PM,plantidtostatename.statename \
from plantinfo \
 INNER JOIN \
(select plantid,statename"+" "+  "from  planttostate \
INNER JOIN (\
select statecode,statename from statecodetoname) AS statecodeandstatename \
ON planttostate.statecode=statecodeandstatename.statecode) AS \
plantidtostatename \
ON plantidtostatename.plantid=plantinfo.plantid \
GROUP BY  plantidtostatename.statename) AS planttostatename \
ON planttostatename.statename =airqualitystate.statename \
WHERE planttostatename.statename = %s;"
        cursor1.execute(query, (statename,))
        res = [json.dumps(dict(record)) for record in cursor1]
        
        return res

    def search_by_plant_name(self,plant_name):
        cursor1 = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "select plantidandstate.plantid, plantidandstate.plantname, noxrate, pmrate, totalcost, totalfuelconsumed, totalgenerated \
from plantinfo \
INNER JOIN ( \
    select plantid, plantname \
from planttostate \
WHERE plantname ILIKE %s \
    ) as plantidandstate  \
ON plantidandstate.plantid = plantinfo.plantid;"
        cursor1.execute(query, ('%'+plant_name+'%',))
        dict_records = cursor1.fetchall()
        
        return dict_records
    
    def countyinformation(self,county_name):
        cursor1 = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query="SELECT statename,averagegooddays,maxno2days,maxpmdays FROM airquality WHERE countyname ILIKE %s"
        cursor1.execute(query, ('%'+county_name+'%',))
        dict_records = cursor1.fetchall()
        return dict_records

    def electricity_consumption(self, state_name):
        client = MongoClient("mongodb://localhost:27017/")
        db = client.powergrid
        collection = db["electricity_consumption"]
        query = {"State": state_name}
        result = list(collection.find(query))

        cursor1 = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = "select sum(totalgenerated) from plantinfo INNER JOIN (select plantid, statename from planttostate INNER JOIN (select statecode,statename from statecodetoname) AS statecodeandstatename ON planttostate.statecode=statecodeandstatename.statecode) AS plantidtostatename ON plantidtostatename.plantid=plantinfo.plantid WHERE plantidtostatename.statename = %s GROUP BY  plantidtostatename.statename;"
        cursor1.execute(query, (state_name,))
       
        res = [json.dumps(dict(record)) for record in cursor1]
        newDict={}
        print(res)
        print(json.loads(res[0]))
        print(result[0])
        newDict['State(MWh)']=result[0]['State'] 
        newDict['Residential(MWh)']= result[0]['Residential'],
        newDict['Commercial(MWh)']=result[0]['Commercial']
        newDict['Industrial(MWh)']=result[0]['Industrial']
        newDict['Transportation(MWh)']=result[0]['Transportation']
        newDict['Total Power Consumed(MWh)']=result[0]['Total']
        newDict['Total Power Generated(MWh)']=json.loads(res[0])['sum']
        print(newDict)
        return newDict

    def insert_new_plant(self, plantid, plantname, statecode, countyname, noxrate, pmrate, totalcost, totalfuelconsumed, totalgenerated):
        try:
            cursor1 = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            count=0
            query1 = "INSERT INTO plantinfo VALUES(%s,%s,%s,%s,%s,%s)"
            cursor1.execute(query1,(plantid,noxrate,pmrate,totalcost,totalfuelconsumed,totalgenerated))
            count=count+cursor1.rowcount

            query2 = "INSERT INTO planttostate VALUES(%s,%s,%s)"
            cursor1.execute(query2,(plantid,statecode,plantname))
            count=count+cursor1.rowcount

            query3 = "INSERT INTO plantidtocounty VALUES(%s,%s)"
            cursor1.execute(query3,(plantid,countyname))
            count=count+cursor1.rowcount

            if count == 3:
                self.conn.commit()
                return "Inserted Successfully"

            else:
                return "There was an error, please check the input variables"
        except:
            return "There was an error, please check the input variables and constraints"
            
