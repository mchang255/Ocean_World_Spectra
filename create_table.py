#This file creates the database and table that belongs in the database. The table will contain minerals' data and information
#To run this file, make sure you are in the same directory as the file and type "python create_table.py" in the terminal window
#As of now, the database will stay local to whoever runs the code. We might move the database to shared server where it is only in one place
#This code should only be run once as attempting to create another database with the same name will bring errors. Should you need to run this code again, please run delete_db.py first

import sqlite3

conn = sqlite3.connect('minspec.db') #connecting to database

c = conn.cursor() #create cursor

#create a table
c.execute("""CREATE TABLE minerals (
    name text,
    chemical_formula text,
    sampleID text,
    sample_purity text,
    wavelengths JSON,
    reflectances JSON
)
""")

# Datatypes:
# NULL
# INTEGER
# REAL - FOR DECIMALS
# TEXT
# BLOB

# Commit our command
conn.commit()

# Close our connection
conn.close()