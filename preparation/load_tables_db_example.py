#!/usr/bin/env python
# coding: utf-

import psycopg2
import pandas as pd
from calendar import monthrange
import time
import re
import os

# connect to database on aws rds: the test database
conn = psycopg2.connect(
    database=<db_name>,
    user=<admin_user_name>,
    password=<db_password>,
    host="<db_host_address>.rds.amazonaws.com",
    port='5432'
)
print ('DB connection established')

print ("Creating table")
cur = conn.cursor()

headers=['ORG_CODE', 'SEX', 'AGE_GROUP_5', 'End_date','register','percentage']

dir_path='/Users/rony/Projects/Health_Geo_app/data/gender_age/with_percentages/'
file_names=os.listdir(dir_path)
print ('file_names:',file_names)

for file_name in file_names:
    file_path='{dp}{fn}'.format(dp=dir_path,fn=file_name)
    table_name=re.sub('\.csv','',file_name)+'t'
    print (file_name,table_name)
    print ('checking null values')

    df = pd.read_csv(file_path)
    print (df.info())

    print ('Creating table')
    statement = """CREATE TABLE {tn} (
        Practice_Code text,
        Sex text,
        Age_Group text,
        Register integer,
        Percentage float,
        End_Date timestamp
        )""".format(tn=table_name)
    print (statement)
    cur.execute(statement)
    conn.commit()

    print ("Loading data to the table")
    f = open(file_path, 'r')
    next (f)
    print (f)
    cur.copy_from(f, '{tn}'.format(tn=table_name), sep=',')
    f.close()
    print (30*'=')
    conn.commit()

conn.close()
