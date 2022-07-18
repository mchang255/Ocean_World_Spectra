# JPL_Code

Where I upload everything JPL!

This respository mainly concerns research in finding surface compositions of ocean worlds in our Solar System (Ceres, Europa, etc.)

All the code I have:

minerals_table.py - will create a database containing many minerals along with wavelengths and reflectances (infrared region). When you "ask" for some minerals, those minerals' information will be returned. Still a work in progress

minerals.txt - what minerals you would like to query

The USGS spectra library is supposed to be here, but in the words of GitHub, "Yowza, that’s a big file. Try again with a file smaller than 25MB." I will link where it can be found: https://crustal.usgs.gov/speclab/QueryAll07a.php (click where it says "usgs_splib07.zip"). Place it in the same directory as minerals_table.py This is needed in order for the code to run!

Also note that for all Python programs, in order to run the code, type: python file_name into a terminal window and press "Enter." I should probably put this at the top of every Python program.
