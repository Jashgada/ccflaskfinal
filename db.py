import csv
import sqlite3

conn = sqlite3.connect('household.db')
cur = conn.cursor()
cur.execute("""DROP TABLE IF EXISTS household""")
cur.execute("""CREATE TABLE household
            (HSHD_NUM integer, L text, AGE_RANGE text, MARITAL text, INCOME_RANGE text, HOMEOWNER text, HSHD_COMPOSITION text, HH_SIZE integer, CHILDREN text)""")

with open('400_households.csv', 'r') as f:
    reader = csv.reader(f.readlines()[1:])  # exclude header line
    cur.executemany("""INSERT INTO household VALUES (?,?,?,?,?,?,?,?,?)""",
                    (row for row in reader))
conn.commit()
conn.close()
