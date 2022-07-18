#This file creates the database and table that belongs in the database. The table will contain minerals' data and information
#Make sure you have mysql downloaded as that is important for housing the database! Download here: https://dev.mysql.com/downloads/mysql/ and select the appropriate package for your computer model
#To run this file, make sure you are in the same directory as the file and type "python create_table.py" in the terminal window
#As of now, the database will stay local to whoever runs the code. We might move the database to shared server where it is only in one place
#This code should only be run once as attempting to create another database with the same name will bring errors. Should you need to run this code again, please run delete_db.py first

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="minspec22"
)

print(mydb)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE minspec") #creating database

mycursor.execute("SHOW DATABASES")

for db in mycursor:
    print(db)
    
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="minspec22",
  database="minspec"
)

mycursor = mydb.cursor()
    
mycursor.execute("CREATE TABLE minerals (name VARCHAR(255), chemical_formula VARCHAR(255), sampleID VARCHAR(255), sample_purity VARCHAR(255), wavelengths JSON, reflectances JSON)") #creating table