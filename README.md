# JPL_Code

Where I upload everything JPL!

This respository mainly concerns research in finding surface compositions of ocean worlds in our Solar System (Ceres, Europa, etc.)

All the code I have:

create_table.py - creates the database and table that houses the minerals' information.

delete_db.py - wipes out existence of database and table. Might be used if you want to start over.

populate_table.py - populates table with minerals' information. Essentially, the table is complete after running this code. Currently just have USGS data. Will add RRUFF data soon.

query_minerals.py - getting the information of the minerals you want from the database.

minerals.txt - what minerals you would like to query. NOT case sensitive, so write however you please (although please spell correctly :) ).

STEPS TO RUN THE CODE:
1. create_table.py
2. populate_table.py
3. query_minerals.py
delete_db.py is optional

OTHER IMPORTANT INFORMATION YOU SHOULD KNOW (especially important is marked with **):

**The USGS spectra library is supposed to be here, but in the words of GitHub, "Yowza, that’s a big file. Try again with a file smaller than 25MB." I will link where it can be found: https://crustal.usgs.gov/speclab/QueryAll07a.php (click where it says "usgs_splib07.zip"). Place it in the same directory as minerals_table.py This is needed in order for the code to run!

**You also need to have MySQL downloaded in order for the code involving the database to work. Go to this link https://dev.mysql.com/downloads/mysql/ and download the appropriate package associated with your computer model.

Also note that for all Python programs, in order to run the code, type: python file_name into a terminal window and press "Enter." Make sure you (when operating the terminal window) are in the same directory as your files! Otherwise, you will need to specify the path of the file. I should probably put this at the top of every Python program.

Code that we may not need anymore:
minerals_table.py - will create a database containing many minerals along with wavelengths and reflectances (infrared region). When you "ask" for some minerals, those minerals' information will be returned. Still a work in progress
