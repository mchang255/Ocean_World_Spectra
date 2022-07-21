# JPL_Code

Where I upload everything JPL!

This respository mainly concerns research in finding surface compositions of ocean worlds in our Solar System (Ceres, Europa, etc.)

All the code I have:

create_table.py - creates the database and table that houses the minerals' information.

populate_table.py - populates table with minerals' information. Essentially, the table is complete after running this code. Currently just have USGS data. Will add RRUFF data soon.

query_minerals.py - getting the information of the minerals you want from the database.

minerals.txt - what minerals you would like to query. NOT case sensitive, so write however you please (although please spell correctly :) ).

STEPS TO RUN THE CODE:
IF THIS IS YOUR FIRST TIME:
1. create_table.py
2. populate_table.py
3. query_minerals.py

EVERY TIME AFTER:
just query_minerals.py

To delete the database, just delete the file that was created (the database is stored in a file). In this case, it would be minspec.db

If you have more information to add to the table...well, I might add an extra file or you will have to modify create_table.py and populate_table.py.

OTHER IMPORTANT INFORMATION YOU SHOULD KNOW (especially important is marked with **):

**Download the minerals you want from USGS here: https://crustal.usgs.gov/speclab/QueryAll07a.php. Search the name in the "Quick Search" bar. We want minerals taken by the NIC spectrometer as that encompasses all the wavelengths in the infrared region. Press "Zip" to download the mineral's data. Extract the wavelengths (you only need one file) and the associated .txt file (ends with RREF.txt) that has the reflectance of the mineral. Place the files in the "minerals" folder. In short, in the "minerals" folder, there should be one wavelengths file and multiple reflectance files.

If minerals have multiple entries, we will choose the sample that is the most pure. We are going by this guide: https://pubs.usgs.gov/ds/1035/ds1035.pdf, page 8. In short, for the NIC4 spectrometer, spectral purity is designated either with a single character for the wavelength range 1.12–6 μm, with two characters for the wavelength ranges 1.12–6 and 6–25 μm, or with three characters for the wavelength ranges 1.12–6, 6–25, and 25–150 μm. For wavelengths longer than 150 μm, spectral purity has not been evaluated (Ex: NIC4aaa). 

What each of the letters mean:

a: The spectrum and sample are pure based on significant supporting data available to the authors. The sample purity from other methods (for example, XRD or microscopic examination) indicate that no contaminants are present. Spectrally, no contaminants are apparent

b: The spectrum of the sample appears pure. However, other sample analyses indicate the presence of other contaminants that may affect reflectance levels to some degree but do not add any significant spectral features in the region evaluated. The spectral features of the primary minerals may have slightly altered intensities, but the feature positions and shapes should be representative

c: The spectrum has some weak features with depths of a few percent or less caused by other contaminants.

d:  Significant spectral contamination. The spectrum is included in the library only because it is the best sample of its type currently available, and because the primary spectral features can still be recognized

u: There are insufficient analyses or knowledge (or both) of the spectral properties of this material to evaluate its spectral purity. In general, we have included such samples because we believe their spectra to be representative.

Some minerals have multiple samples. We want to choose the sample that contains the most information, meaning sample purities assessed for all three regions. If a mineral doesn't have purities for all three regions, we will go with the sample that has two regions assessed, and so on. From there, we choose then choose the sample that is the most pure. Some minerals will have several samples that have the same purity. We will add all of those samples to the database as they may be different grain sizes or their data might be different due to other circumstances.

Also note that for all Python programs, in order to run the code, type: python file_name into a terminal window and press "Enter." Make sure you (when operating the terminal window) are in the same directory as your files! Otherwise, you will need to specify the path of the file. I should probably put this at the top of every Python program.

Code that we may not need anymore:
minerals_table.py - will create a database containing many minerals along with wavelengths and reflectances (infrared region). When you "ask" for some minerals, those minerals' information will be returned. Still a work in progress

delete_db.py - would have deleted the database but this is not needed anymore as we are using sql3ite not MySQL
