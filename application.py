#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from json import dumps
from flask_jsonpify import jsonify
import psycopg2


import psycopg2.extras
import simplejson as json
from database import PowerPlantData 
connection = psycopg2.connect(user = "plantadmin",
                                password = "theadminoftheplant",
                                host = "127.0.0.1",
                                port = "5432",
                                database = "powerplant")



app = Flask(__name__)
api = Api(app)
CORS(app)
class Bolt(Resource):
    
    def get(self):
        cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT statecode, statename FROM statecodetoname")
        records = cursor.fetchall()
        
        return records
class StateEnv(Resource):
    def get(self):
        statename = request.args.get('statename')
        #conn_string="host='localhost' dbname='powerplant' user='plantadmin' password='theadminoftheplant'"
        powerplantData=PowerPlantData()
        #powerplantData.get_air_quality_info_by_state(statename)
        output=powerplantData.get_air_quality_info_by_state(statename)
        return output[0]
class ViewPlants(Resource):
    def get(self):
        plantname = request.args.get('plantname')
        #conn_string="host='localhost' dbname='powerplant' user='plantadmin' password='theadminoftheplant'"
        powerplantData=PowerPlantData()
        #powerplantData.get_air_quality_info_by_state(statename)
        output=powerplantData.search_by_plant_name(plantname)
        return output
    
class ElectricityData(Resource):
    def get(self):
        statename = request.args.get('statename')
        #conn_string="host='localhost' dbname='powerplant' user='plantadmin' password='theadminoftheplant'"
        powerplantData=PowerPlantData()
        #powerplantData.get_air_quality_info_by_state(statename)
        output=powerplantData.electricity_consumption(statename)
        return output

class insertNewPlant(Resource):
    def get(self):
        plantid = request.args.get('plantid')
        plantname = request.args.get('plantname')
        statecode = request.args.get('statecode')
        countyname = request.args.get('countyname')
        noxrate = request.args.get('noxrate')
        pmrate = request.args.get('pmrate')
        totalcost = request.args.get('totalcost')
        totalfuelconsumed = request.args.get('totalfuelconsumed')
        totalgenerated = request.args.get('totalgenerated')
        powerplantData=PowerPlantData()
        #powerplantData.get_air_quality_info_by_state(statename)
        output=powerplantData.insert_new_plant(plantid, plantname, statecode, countyname, noxrate, pmrate, totalcost, totalfuelconsumed, totalgenerated)
        return output 
class countyInformation(Resource):
    def get(self):
        countyname=request.args.get('countyname')
        powerplantData=PowerPlantData()
        output=powerplantData.countyinformation(countyname)
        return output
api.add_resource(Bolt, '/bolt') # Route_1
api.add_resource(StateEnv, '/fetchstateenv') # Route_2
api.add_resource(ViewPlants, '/viewplants') #Route_3
api.add_resource(ElectricityData, '/electricitydata') #Route_4
api.add_resource(insertNewPlant, '/insernewplant') #Route_5
api.add_resource(countyInformation, '/countyinformation') #Route_5



if __name__ == '__main__':
     app.run(port=1300)
        


# In[ ]:




