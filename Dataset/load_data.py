import pandas as pd
import numpy as np
import math
import psycopg2
from io import StringIO
from sqlalchemy import create_engine

def normalizeColumnsForDb(df,columndf,reqcolumndf):
    df=df[columndf].copy()
    j=0
    for i in columndf:
        df.rename(columns = {i:reqcolumndf[j]},inplace=True)
        j=j+1
    return df

def convertToFloat(d):
    if d == ".":
        return 0
    elif d == pd.np.NaN:
        return 0 
    elif math.isnan(d):
        return 0
    else:
        return float(d)

df1=pd.read_excel('DS1.xlsx',sheet_name='8C Air Emissions Control Info',skiprows=4)
columndf1=['Plant ID','NOX Emission Rate\n Entire Year \n(lbs/MMBtu)','PM Emissions Rate \n(lbs/MMBtu)']
reqcolumndf1=['plantid','noxrate','pmrate']
df1=normalizeColumnsForDb(df1,columndf1,reqcolumndf1)

df2=pd.read_excel('DS1.xlsx',sheet_name='8C FGD Operation & Maintenance',skiprows=4)
columndf2=['Plant ID','Total \n(thousand dollars)']
reqcolumndf2=['plantid','totalcost']
df2=normalizeColumnsForDb(df2,columndf2,reqcolumndf2)

df3=pd.read_excel('DS3.xlsx',sheet_name='Page 3 Boiler Fuel Data',skiprows=5)
columndf3=['Plant Id','Total Fuel Consumption\nQuantity']
reqcolumndf3=['plantid','totalfuelconsumed']
df3=normalizeColumnsForDb(df3,columndf3,reqcolumndf3)

df4=pd.read_excel('DS3.xlsx',sheet_name='Page 4 Generator Data',skiprows=5)
columndf4=['Plant Id','Net Generation\nYear To Date']
reqcolumndf4=['plantid','totalgenerated']
df4=normalizeColumnsForDb(df4,columndf4,reqcolumndf4)

df5=pd.read_excel('DS3.xlsx',sheet_name='Page 6 Plant Frame',skiprows=4)
columndf5=['Plant Id','Plant State','Plant Name']
reqcolumndf5=['plantid','statecode','plantname']
df5=normalizeColumnsForDb(df5,columndf5,reqcolumndf5)
df5 = df5.set_index('plantid',drop=True)

df12=df1.set_index('plantid').join(df2.set_index('plantid'),how='outer')
df123=df12.join(df3.set_index('plantid'),how='outer')
df1234=df123.join(df4.set_index('plantid'),how='outer')

columList=list(df1234.columns)

df1234=df1234.reset_index()

columnList=list(df1234.columns)
for i in columnList:
    df1234[i]=df1234[i].apply(lambda d:convertToFloat(d))

df1234=df1234.groupby(['plantid']).mean()
df1234=df1234.reset_index()
df1234['plantid']=df1234['plantid'].apply(lambda l:int(l))
df1234 = df1234.set_index('plantid',drop=True)

df7 = pd.read_csv('annual_aqi_by_county_2017.csv')
columndf7 = ['County','State','Good Days','Days NO2','Days PM2.5']
reqcolumndf7 = ['countyname','statename','averagegooddays','maxno2days','maxpmdays']
df7 = normalizeColumnsForDb(df7, columndf7, reqcolumndf7)
df7 = df7.set_index('countyname',drop=True)

df8 = pd.read_excel('State name to State code.xlsx',sheet_name='SheetJS',skiprows=0)
columndf8 = ['Postal Code','State/District','Abbreviation']
reqcolumndf8 = ['statecode','statename', 'stateabbr']
df8 = normalizeColumnsForDb(df8,columndf8,reqcolumndf8)
df8 = df8.set_index('statecode',drop=True)

df9 = pd.read_excel('2___Plant_Y2017.xlsx',sheet_name='Plant',skiprows=1)
columndf9 = ['Plant Code','County']
reqcolumndf9 = ['plantid','countyname']
df9 = normalizeColumnsForDb(df9,columndf9,reqcolumndf9)
df9 = df9.set_index('plantid',drop=True)

df10 = pd.read_csv('united-states-counties.csv')
columndf10 = ['County','State']
reqcolumndf10 = ['countyname','statename']
df10 = normalizeColumnsForDb(df10,columndf10,reqcolumndf10)
df10 = df10.set_index('countyname',drop=True)

engine = create_engine('postgresql+psycopg2://plantadmin:theadminoftheplant@127.0.0.1:5432/powerplant')

df1234.to_sql('plantinfo', engine, if_exists='append')
df5.to_sql('planttostate', engine, if_exists='append')
df7.to_sql('airquality', engine, if_exists='append')
df8.to_sql('statecodetoname', engine, if_exists='append')
df9.to_sql('plantidtocounty', engine, if_exists='append')
df10.to_sql('countytostate', engine, if_exists='append')