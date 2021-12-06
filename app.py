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




@app.route('/display')
def display():
    sql_statement = """SELECT h.HSHD_NUM, h.L,h.AGE_RANGE,h.MARITAL,h.INCOME_RANGE,h.HOMEOWNER,h.HSHD_COMPOSITION, h.HH_SIZE,h.CHILDREN,t.BASKET_NUM,t.SPEND,t.UNITS,t.STORE_R,t.WEEK_NUM,t.[YEAR],t.PRODUCT_NUM,p.DEPARTMENT,p.COMMODITY FROM household AS h JOIN transactions AS t ON h.HSHD_NUM = t.HSHD_NUM JOIN products AS p ON t.PRODUCT_NUM = p.PRODUCT_NUM WHERE h.HSHD_NUM = '0010'""" 
    cursor = conn.cursor()    
    rows = cursor.execute(sql_statement).fetchall()
    cursor.close()
    formhyptertext = "<p>The household number 10 is </p>"
    formhyptertext += '<br>'.join(str(row) for row in rows)
    formhyptertext += """
    <br>
     <form action="/displayData" method = "POST">
    <p>Sort By <input type = "text" name = "sortBy" /></p>
    <p>You can sort by Hshd_num, Basket_num, Date, Product_num, Department, Commodity</p>
    <p>Search By Household number <input type = "text" name = "search" /></p>
    <p><input type = "submit" value = "Submit" /></p>
</form>
    """
    return formhyptertext
    
@app.route('/displayData/', methods = ["POST", "GET"])
def displayData():
    if request.method == "POST":
        sorter =  request.form["sortBy"]
        if request.form["search"] == "":
            sql_statement = """SELECT h.HSHD_NUM, h.L,h.AGE_RANGE,h.MARITAL,h.INCOME_RANGE,h.HOMEOWNER,h.HSHD_COMPOSITION, h.HH_SIZE,h.CHILDREN,t.BASKET_NUM,t.SPEND,t.UNITS,t.STORE_R,t.WEEK_NUM,t.[YEAR],t.PRODUCT_NUM,p.DEPARTMENT,p.COMMODITY FROM household AS h JOIN transactions AS t ON h.HSHD_NUM = t.HSHD_NUM JOIN products AS p ON t.PRODUCT_NUM = p.PRODUCT_NUM ORDER BY """ + sorter
            
        else:
            
            sql_statement = "SELECT h.HSHD_NUM, h.L,h.AGE_RANGE,h.MARITAL,h.INCOME_RANGE,h.HOMEOWNER,h.HSHD_COMPOSITION, h.HH_SIZE,h.CHILDREN,t.BASKET_NUM,t.SPEND,t.UNITS,t.STORE_R,t.WEEK_NUM,t.[YEAR],t.PRODUCT_NUM,p.DEPARTMENT,p.COMMODITY FROM household AS h JOIN transactions AS t ON h.HSHD_NUM = t.HSHD_NUM JOIN products AS p ON t.PRODUCT_NUM = p.PRODUCT_NUM WHERE h.HSHD_NUM = " + request.form["search"] + " ORDER BY " + sorter
        cursor = conn.cursor()    
        rows = cursor.execute(sql_statement).fetchall()
        cursor.close()
        finstr = "(HSHD_NUM, L, AGE_RANGE, MARITAL, INCOME_RANGE, HOMEOWNER, HSHD_COMPOSITION, HH_SIZE, CHILDREN, BASKET_NUM, SPEND, UNITS, STORE_R, WEEK_NUM, YEAR, PRODUCT_NUM, DEPARTMENT, COMMODITY)<br>"
        finstr += '<br><br>'.join(str(row) for row in rows)
        return finstr
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
         <p>Please beware that large amounts of data may take significant time to load. For effiecient use, try 1000-2000 data points for each table</p>
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
    finstring = """
    <p>
        We can confidently state that customer engagement has been increasing over the last few years. Over the 3 year span from 2018 to 2020, customer spending increases by 0.1585 on average each year. By grouping the data by household number (HSHD_NUM) and by year (YEAR) and then aggregating the data by average spend (SPEND), we can observe the trend below.
    </p>
    <img src="../q1img1.png" alt="graph for q1">
    <p>
        Over the 3 years of data we have, we can observe a flux in various categories of people changing but not in correlation with the customer engagement increase. People who are married or with kids changed their spending habits, but in both groups, their spending was consistent with the known increase in average spend. Therein, we cannot confidently assess that marital status or number of children/presence of children has any effect on the customer engagement.
    </p>
    <img src="../q1img2.png" alt="graph for q1">
    """
    return finstring


@app.route('/retailq2')
def retailQ2():
    finstring = """
     <p>
        The demographic factor that appears to make the biggest impact on customer engagement is income range. Looking at the data displayed, it's easy to tell the relationship between income range and average spend per year is positive. Though the axis labels on the graph are not ordered properly, the income vs. average spend per year reveals that as the income range increases so does the average spend. Per year as well, each income range’s average spend increases with each year. Therein, we can confidently determine that income has a positive impact on customer engagement.
    </p>
    <img src="/q2img1.png" alt="graph for q1">
    <p>
        Another demographic that appears to have an influence on customer engagement is age. Although only one age group stands out, its impact is clear to see in the plot displays. Below, you can observe the average spend per age range per year and the count of all the age groups over the 3 years. Age range 19-24 is the smallest age range, but their average spend is the highest amongst all the age groups. However, when looking at the other age groups, they appear to have similar spending averages and fluctuating engagement.
    </p>
    <img src="/q2img2.png" alt="graph for q1">

    <p>
        In order to drive up customer engagement, we can target the age 19-24 demographic and encourage more young people to shop at Kroger. With their spending average being as high as it is, we’d get more engagement if more young people shopped with us. 
    </p>
    """
    return finstring