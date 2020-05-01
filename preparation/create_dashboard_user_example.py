'''
Create roles privileges for the dashboard users
'''
import psycopg2
import pandas as pd

# Connect to the database as admin
conn = psycopg2.connect(
    database=<db_name>,
    user=<admin_user_name>,
    password=<db_password>,
    host="<db_host_address>.rds.amazonaws.com",
    port='5432'
)
print ('DB connection established')

cur = conn.cursor()

'''
# Revoke privileges statements used in tests
cur.execute("""REVOKE ALL ON ALL TABLES IN SCHEMA public FROM dashboard_user""")
cur.execute ("""REVOKE CONNECT ON DATABASE postgres FROM dashboard_user """)
cur.execute("""REVOKE ALL ON schema public FROM dashboard_user""")
cur.execute ("""DROP ROLE dashboard_user""")
'''

# cur.execute ("""CREATE ROLE dashboard_user WITH LOGIN ENCRYPTED PASSWORD 'healthgeo2020' """)
cur.execute ("""GRANT CONNECT ON DATABASE postgres TO dashboard_user """)
cur.execute ("""GRANT ALL ON schema public TO dashboard_user""")

# Revoke table creation privileges from the user
cur.execute("""REVOKE CREATE ON SCHEMA public FROM dashboard_user""")
# Allow dashboard_user to select data from all table in the database
cur.execute ("""GRANT SELECT ON ALL TABLES IN SCHEMA public TO dashboard_user """)

conn.commit()
conn.close()
print ('DB connection closed')
