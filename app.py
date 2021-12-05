import csv
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
    retString = """
    <form action="">
  <label for="username">Username</label>
  <input type="text" placeholder="Enter Username" name="username" id="username">
  <label for="password">Password:</label>
  <input type="password" name="password" id="password" placeholder="Enter Password">
  <label for="email">Email:</label>
  <input type="email" name="email" id="email" placeholder="Enter Email">
  <button type="submit">Sign up</button>
  <br>
  <p></p>
  <a href="/display">Display Example Data</a>
  <p></p>
  <a href="/loadData"> Load Data</a>
  <p></p>
  <a href="/retailq1"> Retail Question 1</a>
  <p></p>
  <a href="/retailq2"> Retail Question 2</a>
</form>
    """
    return retString

@app.route('/countme/<input_str>')
def count_me(input_str):
    return input_str


@app.route("/test")
def test():
    return "This is test"

@app.route('/query/get')
def post():
        """ Retrieves data from the database """
        sql_statement = "SELECT TOP (1000) * FROM [SalesLT].[Customer]"

        cursor = conn.cursor()    
        rows = cursor.execute(sql_statement).fetchall()
        cursor.close()
        return '<br><br>'.join(str(row) for row in rows)


@app.route('/createDb')
def createDb():
    cursor = conn.cursor()  
    cursor.execute("""DROP TABLE IF EXISTS household""")
    cursor.execute("""CREATE TABLE household (HSHD_NUM nvarchar(MAX), L nvarchar(MAX), AGE_RANGE nvarchar(MAX), MARITAL nvarchar(MAX), INCOME_RANGE nvarchar(MAX), HOMEOWNER nvarchar(MAX), HSHD_COMPOSITION nvarchar(MAX), HH_SIZE nvarchar(MAX), CHILDREN nvarchar(MAX))""")

    with open('400_households.csv', 'r') as f:
        reader = csv.reader(f.readlines()[1:])  # exclude header line
        cursor.executemany("""INSERT INTO household VALUES (?,?,?,?,?,?,?,?,?)""",
                    (row for row in reader))
    return "success!"
@app.route('/display')
def display():
    sql_statement = "SELECT TOP (1000) * FROM [household]"

    cursor = conn.cursor()    
    rows = cursor.execute(sql_statement).fetchall()
    cursor.close()
    return '<br><br>'.join(str(row) for row in rows)

@app.route('/loadData')
def loadData():
    return 'Load Data'

@app.route('/retailq1')
def retailQ1():
    return 'RetailQ1 works'


@app.route('/retailq2')
def retailQ2():
    return 'RetailQ2 works'