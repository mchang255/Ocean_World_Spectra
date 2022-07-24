#The purpose of this code is to populate the table with the information we have. So far, we just have the USGS speclib, and this program compiles their wavelength, reflectance data, along with other miscellaneous information about the mineral (i.e. chemical formula)
#To run this file, make sure you are in the same directory as the file and type "python populate_table.py" in the terminal window
#Make sure you have run create_table.py first as we need to have the database and table already set up
#Make sure you have the appropriate mineral files downloaded. Go here: https://crustal.usgs.gov/speclab/QueryAll07a.php?
#This code should only be run once as running again will cause duplicates in the table. Should you need to run this code again, please run delete_db.py first and then create_table.py.

import numpy as np
import os
import re
import requests
from subprocess import call
import matplotlib.pyplot as plt
import subprocess
import sqlite3

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
usgs_dir = os.path.relpath(os.path.join(os.path.dirname(__file__),'usgs'))

call ('rm -rf ' + usgs_dir + '/.ipynb_checkpoints', shell=True)

wavelengths = np.loadtxt(os.path.join(usgs_dir,'splib07a_Wavelengths_NIC4_Nicolet_1.12-216microns.txt'), skiprows=1, unpack=True)

all_minerals = os.listdir(usgs_dir)

chemical_formulas = []
reflectances = []
names = []
relevant_wavelengths = []
samp_purity = []
samp_id = []


for i in range(len(all_minerals)):
    if 'RREF' in all_minerals[i]:
        reflectance = np.loadtxt(os.path.join(usgs_dir, all_minerals[i]), skiprows=1, unpack=True)
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
        
#For minerals found in RRUFF
rruff_dir = os.path.relpath(os.path.join(os.path.dirname(__file__),'rruff'))

call ('rm -rf ' + rruff_dir + '/.ipynb_checkpoints', shell=True)
all_minerals_rruff = os.listdir(rruff_dir)

for j in range(len(all_minerals_rruff)):
    rruff_file = os.path.join(rruff_dir, all_minerals_rruff[j])
    rruff_wavenum, rruff_refl = np.loadtxt(rruff_file, delimiter = ", ", unpack=True)
    rruff_wavelength = 10000 / rruff_wavenum
    
    with open(rruff_file, 'r') as rruff:
        lines = rruff.readlines()
        for line in lines:
            index = line.find('=')
            if 'NAMES' in line[:index]:
                rruff_name = str(line[index+1:].strip())
            elif 'RRUFFID' in line[:index]:
                rruff_id = str(line[index+1:].strip())
            elif 'IDEAL CHEMISTRY' in line[:index]:
                rruff_chem = str(line[index+1:].strip())
    
    chemical_formulas.append(rruff_chem)
    reflectances.append(rruff_refl)
    names.append(rruff_name)
    relevant_wavelengths.append(rruff_wavelength)
    samp_purity.append('Not given by RRUFF')
    samp_id.append(rruff_id)


#adding info to database
conn = sqlite3.connect('minspec.db')

c = conn.cursor()

for a in range(len(names)):
    c.execute("INSERT INTO minerals VALUES ('" + names[a] + "', '" + chemical_formulas[a] + "', '" + samp_id[a] + "', '" + samp_purity[a] + "', '" + str(list(relevant_wavelengths[a])) + "', '" + str(list(reflectances[a])) + "')")

conn.commit()

conn.close()