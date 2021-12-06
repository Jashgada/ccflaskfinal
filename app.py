import csv
# import os
# import json
from flask import Flask, request
import pyodbc
# import pandas as pd
# from flask_restful import reqparse, Api

conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};Server=tcp:cloudprojdb.database.windows.net,1433;Database=cloudprojdb;Uid=adminuser;Pwd=bingus12uwu.;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")
# conn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:cloudfinalprojectf21.database.windows.net,1433;Database=FinalProjectDB;Uid=liz;Pwd=lilmems!;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")


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



# @app.route('/createDb')
# def createDb():
#     cursor = conn.cursor()  
#     cursor.execute("""DROP TABLE IF EXISTS household""")
#     cursor.execute("""CREATE TABLE household (HSHD_NUM nvarchar(MAX), L nvarchar(MAX), AGE_RANGE nvarchar(MAX), MARITAL nvarchar(MAX), INCOME_RANGE nvarchar(MAX), HOMEOWNER nvarchar(MAX), HSHD_COMPOSITION nvarchar(MAX), HH_SIZE nvarchar(MAX), CHILDREN nvarchar(MAX))""")

#     with open('400_households.csv', 'r') as f:
#         reader = csv.reader(f.readlines()[1:])  # exclude header line
#         cursor.executemany("""INSERT INTO household VALUES (?,?,?,?,?,?,?,?,?)""",
#                     (row for row in reader))
#     cursor.commit()
#     cursor.close()
#     return "success!"

@app.route('/display')
def display():
    formhyptertext = """
     <form action="/displayData" method = "POST">
    <p>Sort By <input type = "text" name = "sortBy" /></p>
    <p>Yyou can sort by Hshd_num, Basket_num, Date, Product_num, Department, Commodity</p>
    <p><input type = "submit" value = "Submit" /></p>
</form>
    """
    return formhyptertext
    # sql_statement = "SELECT TOP (1000) * FROM [household]"

    # cursor = conn.cursor()    
    # rows = cursor.execute(sql_statement).fetchall()
    # cursor.close()
    # return '<br><br>'.join(str(row) for row in rows)
@app.route('/displayData/', methods = ["POST", "GET"])
def displayData():
    if request.method == "POST":
        sorter =  request.form["sortBy"]
        sql_statement = """SELECT TOP (1000) * FROM [household] WHERE HSHD_NUM='0010' ORDER BY """ + sorter #ORDER BY " + sorter + "WHERE HSHD_NUM='0010'"
        cursor = conn.cursor()    
        rows = cursor.execute(sql_statement).fetchall()
        cursor.close()
        return '<br><br>'.join(str(row) for row in rows)
    if request.method == "GET":
        return "directly trying to access data"
    return "Fail"

@app.route('/displayData/', methods = ["POST", "GET"])
def displayData():
    if request.method == "POST":
        sorter =  request.form["sortBy"]
        sql_statement = """SELECT TOP (1000) * FROM [household] WHERE HSHD_NUM='0010' ORDER BY """ + sorter #ORDER BY " + sorter + "WHERE HSHD_NUM='0010'"
        cursor = conn.cursor()    
        rows = cursor.execute(sql_statement).fetchall()
        cursor.close()
        return '<br><br>'.join(str(row) for row in rows)
    if request.method == "GET":
        return "directly trying to access data"
    return "Fail"


def makeHouseHoldDb():
    cursor = conn.cursor()  
    cursor.execute("""DROP TABLE IF EXISTS household""")
    cursor.execute("""CREATE TABLE household (HSHD_NUM nvarchar(MAX), L nvarchar(MAX), AGE_RANGE nvarchar(MAX), MARITAL nvarchar(MAX), INCOME_RANGE nvarchar(MAX), HOMEOWNER nvarchar(MAX), HSHD_COMPOSITION nvarchar(MAX), HH_SIZE nvarchar(MAX), CHILDREN nvarchar(MAX))""")

    with open('userHousehold.csv', 'r') as f:
        reader = csv.reader(f.readlines()[1:])  # exclude header line
        cursor.executemany("""INSERT INTO household VALUES (?,?,?,?,?,?,?,?,?)""",
                    (row for row in reader))
    conn.commit()
    cursor.close()

def makeProductsDb():
    cursor = conn.cursor()  
    cursor.execute("""DROP TABLE IF EXISTS products""")
    cursor.execute("""CREATE TABLE products (PRODUCT_NUM nvarchar(MAX), DEPARTMENT nvarchar(MAX), COMMODITY nvarchar(MAX), BRAND_TY nvarchar(MAX), NATURAL_ORGANIC_FLAG nvarchar(MAX))""")
    with open('userProducts.csv', 'r') as f:
        reader = csv.reader(f.readlines()[1:])  # exclude header line
        cursor.executemany("""INSERT INTO products VALUES (?,?,?,?,?)""",
                    (row for row in reader))
    conn.commit()
    cursor.close()

def makeTransactionsDb():
    cursor = conn.cursor()  
    cursor.execute("""DROP TABLE IF EXISTS transactions""")
    cursor.execute("""CREATE TABLE transactions (BASKET_NUM nvarchar(MAX), HSHD_NUM nvarchar(MAX), PURCHASE_ nvarchar(MAX),	PRODUCT_NUM nvarchar(MAX),  SPEND nvarchar(MAX), UNITS nvarchar(MAX), STORE_R nvarchar(MAX), WEEK_NUM nvarchar(MAX),YEAR nvarchar(MAX))""")

    with open('userTransactions.csv', 'r') as f:
        reader = csv.reader(f.readlines()[1:])  # exclude header line
        cursor.executemany("""INSERT INTO transactions VALUES (?,?,?,?,?,?,?,?,?)""",
                    (row for row in reader))
    cursor.commit()
    cursor.close()

@app.route('/loadData')
def loadData():
    return """<form action = "/uploader" method = "POST" 
         enctype = "multipart/form-data">
         <p> Household file: <input type = "file" name = "householdFile" /></p>
         <p> Products file: <input type = "file" name = "productsFile" /></p>
         <p> Transactions file: <input type = "file" name = "transactionsFile" /></p>
         <input type = "submit"/>
      </form>""" 

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['householdFile']
      g = request.files['productsFile']
      h = request.files['transactionsFile']

      g.filename = "userProducts.csv"
      g.save(g.filename)
      g.close()
      makeProductsDb()
      
      f.filename = "userHousehold.csv"
      f.save(f.filename)
      f.close()
      makeHouseHoldDb()

      
      h.filename = "userTransactions.csv"
      h.save(h.filename)
      h.close()
      makeTransactionsDb()
      
      return 'file uploaded successfully'

@app.route('/retailq1')
def retailQ1():
    return 'RetailQ1 works'


@app.route('/retailq2')
def retailQ2():
    return 'RetailQ2 works'