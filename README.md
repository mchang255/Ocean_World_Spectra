# Ocean World Spectra Code

Hello!

This respository mainly concerns research in finding surface compositions of ocean worlds in our Solar System (Ceres, Europa, etc.)

All the code I have:

create_table.py - creates the database and table that houses the minerals' information.

populate_table.py - populates table with minerals' information. Essentially, the table is complete after running this code. Currently just have USGS data. Will add RRUFF data soon.

query_minerals.py - getting the information of the minerals you want from the database.

linear_mixing.py - mixing and unmixing mineral compositions (mainly tailored to the data in salt_volumes, which are models of salts on Europa) and produces figures of the spectra of the mixtures at each temperature as the proportions change with temperature

mcr.py - an unmixing method that uses multivariate curve resolution (MCR). It is currently used within linear_mixing.py as it requires some variables in that script. Cannot stand on its own at the moment.

percent_error_mixtures.py - calculates the absolute percentage difference between the actual and predicted proportions and produces figures on how the percentage difference varies with temperature and mineral

minerals.txt - what minerals you would like to query. NOT case sensitive, so write however you please (although please spell correctly :) ).

linear_mixing.txt - what minerals you would like to mix. The ID of the mineral also needs to be specified (to find ID, view the data file associated with the mineral in the mineral_data folder)

linear_mixing_param.txt - specifying what mineral mixture type is needed (fractional or equilibrium) and what kind of guess estimate to use for unmixing (end-member spectra or guess proportions/percentages)

percent_error_minerals.txt - what minerals you would like to compare the predicted and actual proportions of. All the minerals you list should be in a mixture together.

whole_library.txt - specifies what minerals will be part of the "library" that the MCR program will peruse through and select what minerals it thinks are in the mixture. In real life research, we don't know what we are looking at, so inputting a huge library of minerals is to reflect that uncertainty.

STEPS TO RUN THE CODE:
IF THIS IS YOUR FIRST TIME:
1. create_table.py
2. populate_table.py
3. query_minerals.py
4. linear_mixing.py
5. percent_error_mixtures.py

EVERY TIME AFTER:
just steps 3 - 5

To delete the database, just delete the file that was created (the database is stored in a file). In this case, it would be minspec.db

If you have more information to add to the table...well, I might add an extra file or you will have to modify create_table.py and populate_table.py.

Please view the individual files for more details and steps as for what is required.

OTHER IMPORTANT INFORMATION YOU SHOULD KNOW (especially important is marked with **):

**Download the minerals you want from USGS here: https://crustal.usgs.gov/speclab/QueryAll07a.php. Search the name in the "Quick Search" bar. We want minerals taken by the NIC spectrometer as that encompasses all the wavelengths in the infrared region. Press "Zip" to download the mineral's data. Extract the wavelengths (you only need one file) and the associated .txt file (ends with RREF.txt) that has the reflectance of the mineral. Place the files in the "usgs" folder. In short, in the "usgs" folder, there should be one wavelengths file and multiple reflectance files.

**If there are minerals you want but that cannot be found in USGS, go to RRUFF: https://rruff.info. Search the name in the "Mineral" bar. If there is only one sample, that result will immediately pop up or if there are multiple samples, a list of them will pop up, in which case you will have individually select which sample you would like view. We ONLY want minerals that contain infrared data. Some of the samples might have their data broken up as certain spectrometers might only work with certain regions of the IR spectra, in which case we will only download the portion concerning shorter wavelengths (~<25 microns). If there are mulitple samples with IR spectra, then we want the one that is most pure, and the way to check is by looking at the Microprobe Data File and looking at the standard deviation and/or comparing the ideal and measured chemistries. In case the Microprobe Data File is not available, the measured chemistry should be listed there. In case the measured chemistry is not listed, then we go by description (ex: color, etc.). For example, there is a quartz entry that contains rose quartz, which is clearly indicative of contamination. This is not a good sample. If there is no other tiebreaker, download all samples. Place all files in the "rruff" folder.

**w3m is a Unix command that is used in populate_table.py to fetch the chemistry of minerals we found in USGS by going to the web page and extracting the formula. I don't believe this is command is automatically installed on all computers. One way to install is doing brew install w3m. You can also try sudo apt install w3m.

FOR USGS, if minerals have multiple entries, we will choose the sample that is the most pure. We are going by this guide: https://pubs.usgs.gov/ds/1035/ds1035.pdf, page 8. In short, for the NIC4 spectrometer, spectral purity is designated either with a single character for the wavelength range 1.12–6 μm, with two characters for the wavelength ranges 1.12–6 and 6–25 μm, or with three characters for the wavelength ranges 1.12–6, 6–25, and 25–150 μm. For wavelengths longer than 150 μm, spectral purity has not been evaluated (Ex: NIC4aaa). 

What each of the letters mean:

a: The spectrum and sample are pure based on significant supporting data available to the authors. The sample purity from other methods (for example, XRD or microscopic examination) indicate that no contaminants are present. Spectrally, no contaminants are apparent

b: The spectrum of the sample appears pure. However, other sample analyses indicate the presence of other contaminants that may affect reflectance levels to some degree but do not add any significant spectral features in the region evaluated. The spectral features of the primary minerals may have slightly altered intensities, but the feature positions and shapes should be representative

c: The spectrum has some weak features with depths of a few percent or less caused by other contaminants.

d:  Significant spectral contamination. The spectrum is included in the library only because it is the best sample of its type currently available, and because the primary spectral features can still be recognized

u: There are insufficient analyses or knowledge (or both) of the spectral properties of this material to evaluate its spectral purity. In general, we have included such samples because we believe their spectra to be representative.

Some minerals have multiple samples. We want to choose the sample that contains the most information, meaning sample purities assessed for all three regions. If a mineral doesn't have purities for all three regions, we will go with the sample that has two regions assessed, and so on. From there, we choose then choose the sample that is the most pure. Some minerals will have several samples that have the same purity. We will add all of those samples to the database as they may be different grain sizes or their data might be different due to other circumstances.

What is Multivariate Curve Resolution (MCR)?
This method involves assuming the resulting mixture to be a linear combination of the individual end-members that make it up. Since we have many samples mixed in different proportions, we can place all those samples into a matrix, and every row of the matrix is a mixture. MCR then decomposes that matrix into one matrix containing the concentrations and another with the individual end-member spectra. There is always going to be some residual error, and MCR tries to minimize that error by performing as many iterations as indicated. Source: https://mdatools.com/docs/mcr.html

Also note that for all Python programs, in order to run the code, type: python file_name into a terminal window and press "Enter." Make sure you (when operating the terminal window) are in the same directory as your files! Otherwise, you will need to specify the path of the file. I should probably put this at the top of every Python program.

NONLINEAR MATLAB PROGRAM: Markov Chain Monte Carlo (MCMC) Hapke Program. Currently in the works!

NOTE: There are two different directories for the MCMC programs. One of them has the suffix "original." This is the original code published by Lapôtre et al. The other code is me altering the original and playing around with it (i.e. modifying the code so it can process hundreds of files automatically). At this moment, I might go back to the original.

Code that we may not need anymore:

minerals_table.py - will create a database containing many minerals along with wavelengths and reflectances (infrared region). When you "ask" for some minerals, those minerals' information will be returned. Still a work in progress

delete_db.py - would have deleted the database but this is not needed anymore as we are using sql3ite not MySQL

SPECIAL THANKS:

Dr. Laura Rodriguez from the Origins and Habitability Lab at Jet Propulsion Laboratory for the MCR code. It was a huge milestone in this project.

Dr. Marc Neveu from NASA Goddard for the Europa salt data.

Dr. Mathieu Lapôtre et al. for the Hapke unmixing model

United States Geological Survey (USGS)

Raman Research Used for Fun (RRUFF)

Paul Johnson et al. for hydrohalite data

Katrin Stephan et al. for water ice data

Helen Maynard-Casely et al. for meridianiite data

Martha Gilmore et al. for ikaite data


