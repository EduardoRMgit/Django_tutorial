import os
import psycopg2
import datetime

conn_params = {'database': 'template1', 'user': os.getenv('POSTGRES_USER'),
               'password': os.getenv('POSTGRES_PASSWORD'),
               'host': os.getenv('POSTGRES_HOST'),
               'port': os.getenv('POSTGRES_PORT', 5432)}

name = os.getenv('POSTGRES_NAME', 'brattdev')

try:
    conn = psycopg2.connect(**conn_params)
except Exception as e:
    print(e)

conn.set_isolation_level(0)

cur = conn.cursor()

error = True
now = datetime.datetime.now()
deltaT = 0

while error and deltaT < 60:
    deltaT = (datetime.datetime.now() - now).seconds
    try:
        cur.execute("""
            select pg_terminate_backend(pid)
            from pg_stat_activity
            where
            datname = '""" + name + """';
        """)
        cur.execute("""DROP DATABASE """ + name)
        print("deleted db " + name)
        error = False
    except Exception as e:
        print(e)
    try:
        cur.execute("""CREATE DATABASE """ + name)
        error = False
    except Exception as e:
        print(e)
