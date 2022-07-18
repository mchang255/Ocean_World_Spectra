#The purpose of this program is to completely wipe the database + table that you have created in create_table.py. The point of this is if in case you make a mistake that requires the code being run twice or the table is populated with a lot of information you don't want, and it's beyond repair, you can just start over using this code. Kind of like a fail-safe
#To run this program, make sure you are in the directory of the program and minerals.txt and type 'python delete_db.py' in the terminal

import mysql.connector
    
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="minspec22",
  database="minspec"
)

mycursor = mydb.cursor()

mycursor.execute('DROP DATABASE IF EXISTS minspec')