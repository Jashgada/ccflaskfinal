# import csv
# import os
# import json
from flask import Flask
import pyodbc
# import pandas as pd
# from flask_restful import reqparse, Api

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:cloudprojdb.database.windows.net,1433;Database=cloudprojdb;Uid=adminuser;Pwd=bingus12uwu.;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")

app = Flask(__name__)
app.config.from_object(__name__)

# api = Api(app)

# conn = pyodbc.connect(os.environ['SQLAZURECONNSTR_WWIF'])
@app.route("/")
def hello():
    return "Hello, World cdci!"

@app.route('/countme/<input_str>')
def count_me(input_str):
    return input_str


@app.route("/test")
def test():
    return "This is test"

# @app.route('/query/get')
# def post():
#         """ Retrieves data from the database """
#         sql_statement = "SELECT TOP (1000) * FROM [SalesLT].[Customer]"

#         cursor = conn.cursor()    
#         rows = cursor.execute(sql_statement).fetchall()
#         cursor.close()
#         return '<br><br>'.join(str(row) for row in rows)
        