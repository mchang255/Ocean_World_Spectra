#The purpose of this code is to populate the table with the information we have. So far, we just have the USGS speclib, and this program compiles their wavelength, reflectance data, along with other miscellaneous information about the mineral (i.e. chemical formula)
#To run this file, make sure you are in the same directory as the file and type "python populate_table.py" in the terminal window
#Make sure you have run create_table.py first as we need to have the database and table already set up
#Make sure you have the USGS library downloaded
#This code should only be run once as running again will cause duplicates in the table. Should you need to run this code again, please run delete_db.py first and then create_table.py.

import mysql.connector
import numpy as np
import os
import re
import requests
from subprocess import call
import matplotlib.pyplot as plt
import subprocess

#https://stackoverflow.com/questions/5419204/index-of-duplicates-items-in-a-python-list - this function tells what indices are duplicates in a list
def list_duplicates_of(seq,item):
    start_at = -1
    locs = []
    while True:
        try:
            loc = seq.index(item,start_at+1)
        except ValueError:
            break
        else:
            locs.append(loc)
            start_at = loc
    return locs

#For minerals found in USGS database
#loading in files
usgs_dir = os.path.relpath(os.path.join(os.path.dirname(__file__),'usgs_splib07','ASCIIdata','ASCIIdata_splib07a'))

wavelengths = np.loadtxt(os.path.join(usgs_dir,'splib07a_Wavelengths_NIC4_Nicolet_1.12-216microns.txt'), skiprows=1, unpack=True)

minerals_dir = os.path.relpath(os.path.join(usgs_dir,'ChapterM_Minerals'))

all_minerals = os.listdir(minerals_dir)

chemical_formulas = []
reflectances = []
names = []
relevant_wavelengths = []
samp_purity = []
samp_id = []


for i in range(len(all_minerals)):
    if 'RREF' in all_minerals[i]:
        reflectance = np.loadtxt(os.path.join(minerals_dir, all_minerals[i]), skiprows=1, unpack=True)
        channel_BA = (reflectance != -1.2300000e+034) #if one of the channels is this value, that means it is strongly affected by atmospheric absorption and must have been deleted
        channel_wavelengths = wavelengths[channel_BA] #getting the relevant wavelengths that have values for                                                                  reflectance
        channel_reflectance = reflectance[channel_BA]
        
        reflectances.append(channel_reflectance)
        relevant_wavelengths.append(channel_wavelengths)
        
        new_name = all_minerals[i].split('_')[1]
        
        names.append(new_name) #attempting to get chemical formulas by searching their USGS pages and finding the formula. However, the current method I'm using for some reason doesn't produce the full HTML page...
        
        new_replacement = all_minerals[i].replace('.txt', '.html')
        new_replacement = new_replacement[9:]
        
        samp_purity.append(all_minerals[i].split('_')[-2])
        
        result = re.search(new_name + '_(.*)_NIC', all_minerals[i])
            
        samp_id.append(result.group(1))
        
        #Getting chemical formula of mineral by going to the USGS page for each of the mineral
        
        link = "https://crustal.usgs.gov/speclab/data/HTMLmetadata/" + new_replacement
        
        link = link.replace('(', '\(')
        link = link.replace(')', '\)')
        link = link.replace('%', 'percent')
        link = link.replace('#', '%23')
        
        call('echo ' + link + '', shell=True)
        
        formula = subprocess.check_output('w3m -dump ' + link + ' | grep \'FORMULA:\' | sed \'s/FORMULA://\' | tr -d "[:blank:]"', shell=True) #brew install w3m if you don't have it
        formula = str(formula)
        formula = formula.replace('b\'', '')
        formula = formula.replace('\\n\'', '')
        
        if formula == '\'':
            formula = "Unknown"
        
        print(formula)
        
        chemical_formulas.append(formula)

#if minerals have multiple entries, we will choose the sample that is the most pure. We are going by this guide: https://pubs.usgs.gov/ds/1035/ds1035.pdf, page 8. In short, for the NIC4 spectrometer, spectral purity is designated either with a single character for the wavelength range 1.12–6 μm, with two characters for the wavelength ranges 1.12–6 and 6–25 μm, or with three characters for the wavelength ranges 1.12–6, 6–25, and 25–150 μm. For wavelengths longer than 150 μm, spectral purity has not been evaluated (Ex: NIC4aaa).
#What each of the letters mean:
# a: The spectrum and sample are pure based on significant supporting data available to the authors. The sample purity from other methods (for example, XRD or microscopic examination) indicate that no contaminants are present. Spectrally, no contaminants are apparent
# b: The spectrum of the sample appears pure. However, other sample analyses indicate the presence of other contaminants that may affect reflectance levels to some degree but do not add any significant spectral features in the region evaluated. The spectral features of the primary minerals may have slightly altered intensities, but the feature positions and shapes should be representative
# c: The spectrum has some weak features with depths of a few percent or less caused by other contaminants.
# d:  Significant spectral contamination. The spectrum is included in the library only because it is the best sample of its type currently available, and because the primary spectral features can still be recognized
# u: There are insufficient analyses or knowledge (or both) of the spectral properties of this material to evaluate its spectral purity. In general, we have included such samples because we believe their spectra to be representative.
#Some minerals have multiple samples. We want to choose the sample that contains the most information, meaning sample purities assessed for all three regions. If a mineral doesn't have purities for all three regions, we will go with the sample that has two regions assessed, and so on. From there, we choose then choose the sample that is the most pure. Some minerals will have several samples that have the same purity. We will add all of those samples to the database as they may be different grain sizes or their data might be different due to other circumstances.

purest_names = []
purest_wavelengths = []
purest_reflectances = []
purest_purities = []
purest_id = []
purest_formulas = []
res = []


for j in range(len(names)): #seeing what minerals have multiple entries
    print(names[j] + ' has indices of ' + str(list_duplicates_of(names,names[j])))
    indices = list_duplicates_of(names,names[j])
    res.append(indices)
    
duplicates = []
for i in res:
    if i not in duplicates:
        duplicates.append(i)

more_duplicates = []

#selecting the most pure sample
for n in range(len(duplicates)):
    pure_samp_codes = []
    pure_samp_codes_length = []
    if len(duplicates[n]) > 1: #if there's more than one sample
        for k in range(len(duplicates[n])):
            samps = samp_purity[duplicates[n][k]]
            pure_samp_codes.append(samps)
            
        for s in range(len(pure_samp_codes)):
            length_string = len(pure_samp_codes[s])
            pure_samp_codes_length.append(length_string)
            
        most_specific = np.max(pure_samp_codes_length)
        index_longest = list_duplicates_of(pure_samp_codes_length,most_specific)
        
        sums = []
        
        for r in index_longest:
            purity_sum = sum(ord(l) for l in pure_samp_codes[r])
            print(pure_samp_codes[r])
            print(purity_sum)
            sums.append(purity_sum)
        
        most_pure = np.min(sums)
        purest_index = list_duplicates_of(sums,most_pure)
        
        for q in purest_index:
            index_to_use = duplicates[n][index_longest[q]]
            purest_names.append(names[index_to_use])
            purest_wavelengths.append(relevant_wavelengths[index_to_use])
            purest_reflectances.append(reflectances[index_to_use])
            purest_purities.append(samp_purity[index_to_use])
            purest_id.append(samp_id[index_to_use])
            purest_formulas.append(chemical_formulas[index_to_use])
    else:
        purest_names.append(names[duplicates[n][0]])
        purest_wavelengths.append(relevant_wavelengths[duplicates[n][0]])
        purest_reflectances.append(reflectances[duplicates[n][0]])
        purest_purities.append(samp_purity[duplicates[n][0]])
        purest_id.append(samp_id[duplicates[n][0]])
        purest_formulas.append(chemical_formulas[duplicates[n][0]])
                  
        
for j in range(len(purest_names)):
    print(purest_names[j] + ' has purity codes of ' + purest_purities[j] + '. Its sample ID: ' + purest_id[j])

#adding info to database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="minspec22",
  database="minspec"
)

mycursor = mydb.cursor()

for a in range(len(purest_names)):
    mycursor.execute("INSERT INTO minerals (name, chemical_formula, sampleID, sample_purity, wavelengths, reflectances) VALUES ('" + purest_names[a] + "', '" + purest_formulas[a] + "', '" + purest_id[a] + "', '" + purest_purities[a] + "', '" + str(list(purest_wavelengths[a])) + "', '" + str(list(purest_reflectances[a])) + "')")

mydb.commit()