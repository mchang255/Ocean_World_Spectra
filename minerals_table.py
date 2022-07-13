import numpy as np
import os
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
from subprocess import call
import matplotlib.pyplot as plt

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
#loading in viles
usgs_dir = os.path.relpath(os.path.join(os.path.dirname(__file__),'usgs_splib07','ASCIIdata','ASCIIdata_splib07a'))

wavelengths = np.loadtxt(os.path.join(usgs_dir,'splib07a_Wavelengths_NIC4_Nicolet_1.12-216microns.txt'), skiprows=1, unpack=True)

minerals_dir = os.path.relpath(os.path.join(usgs_dir,'ChapterM_Minerals'))

all_minerals = os.listdir(minerals_dir)

chemical_formulas = []
reflectances = []
names = []
relevant_wavelengths = []
samp_purity = []


for i in range(len(all_minerals)):
    if 'RREF' in all_minerals[i]:
        reflectance = np.loadtxt(os.path.join(minerals_dir, all_minerals[i]), skiprows=1, unpack=True)
        channel_BA = (reflectance != -1.2300000e+034) #if one of the channels is this value, that means it is strongly affected by atmospheric absorption and must have been deleted
        channel_wavelengths = wavelengths[channel_BA] #getting the relevant wavelengths that have values for                                                                  reflectance
        channel_reflectance = reflectance[channel_BA]
        
        reflectances.append(channel_reflectance)
        relevant_wavelengths.append(channel_wavelengths)
        
        names.append(all_minerals[i].split('_')[1]) #attempting to get chemical formulas by searching their USGS pages                                                     and finding the formula. However, the current method I'm using for                                                     some reason doesn't produce the full HTML page...
        
        new_replacement = all_minerals[i].replace('.txt', '.html')
        new_replacement = new_replacement[9:]
        
        samp_purity.append(all_minerals[i].split('_')[-2])
        
        #link = "https://crustal.usgs.gov/speclab/data/HTMLmetadata/" + new_replacement
        
        
        
#         link = "https://en.wikipedia.org/wiki/" + all_minerals[i].split('_')[1]
        
#         call('echo ' + link + '', shell=True)
        
#         call('curl --silent ' + link, shell=True)

#if minerals have multiple entries, we will choose the sample that is the most pure. We are going by this guide: https://pubs.usgs.gov/ds/1035/ds1035.pdf, page 8. In short, for the NIC4 spectrometer, spectral purity is designated either with a single character for the wavelength range 1.12–6 μm, with two characters for the wavelength ranges 1.12–6 and 6–25 μm, or with three characters for the wavelength ranges 1.12–6, 6–25, and 25–150 μm. For wavelengths longer than 150 μm, spectral purity has not been evaluated (Ex: NIC4aaa).
#What each of the letters mean
# a: The spectrum and sample are pure based on significant supporting data available to the authors. The sample purity from other methods (for example, XRD or microscopic examination) indicate that no contaminants are present. Spectrally, no contaminants are apparent
# b: The spectrum of the sample appears pure. However, other sample analyses indicate the presence of other contaminants that may affect reflectance levels to some degree but do not add any significant spectral features in the region evaluated. The spectral features of the primary minerals may have slightly altered intensities, but the feature positions and shapes should be representative
# c: The spectrum has some weak features with depths of a few percent or less caused by other contaminants.
# d:  Significant spectral contamination. The spectrum is included in the library only because it is the best sample of its type currently available, and because the primary spectral features can still be recognized
# u: There are insufficient analyses or knowledge (or both) of the spectral properties of this material to evaluate its spectral purity. In general, we have included such samples because we believe their spectra to be representative.

purest_names = []
purest_wavelengths = []
purest_reflectances = []
purest_purities = []
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


#getting rid of duplicates and extracting the purest sample. the criteria for greatest purity is if two samples have the same number of characters for purities, then we choose the sample that has most amount of "least-valued" (ex: a would beat c) characters.
#if two sample don't have the same amount of characters, then we will go with the sample that has the most amount of characters??
#THIS WILL PROBABLY BE DELETED
# for n in range(len(duplicates)):
#     if len(duplicates[n]) > 1:
#         for k in range(len(duplicates[n])):
#             current_samp = samp_purity[duplicates[n][k]]
#             print(names[duplicates[n][k]] + ' has a spectrometer code ' + current_samp + ' and index ' + str(duplicates[n][k]))
#             if k == 0:
#                 purest_samp = samp_purity[duplicates[n][0]]
#                 purest_index = duplicates[n][k]
#                 continue
#             else:
#                 current_sum = sum([ord(l) for l in current_samp]) #taken from https://stackoverflow.com/questions/28182454/multiple-characters-in-python-ord-function
#                 purest_sum = sum(ord(m) for m in purest_samp)
                
#                 print('(Current sum) The sum of ' + current_samp + ' is ' + str(current_sum))
#                 print('(Pure sum) The sum of ' + purest_samp + ' is ' + str(purest_sum))
                
#                 if current_sum > purest_sum:
#                     continue
#                 else:
#                     purest_samp = samp_purity[duplicates[n][k]]
#                     purest_index = duplicates[n][k]
#         print('The purest sample has a spectrometer code of ' + str(samp_purity[purest_index]))
#         purest_names.append(names[purest_index])
#         purest_wavelengths.append(relevant_wavelengths[purest_index])
#         purest_reflectances.append(reflectances[purest_index])
#         purest_purities.append(samp_purity[purest_index])
#     else:
#         purest_names.append(names[duplicates[n][0]])
#         purest_wavelengths.append(relevant_wavelengths[duplicates[n][0]])
#         purest_reflectances.append(reflectances[duplicates[n][0]])
#         purest_purities.append(samp_purity[duplicates[n][0]])
        
for n in range(len(duplicates)):
    if len(duplicates[n]) > 1:
        for k in range(len(duplicates[n])):
            current_samp = samp_purity[duplicates[n][k]]
            print(names[duplicates[n][k]] + ' has a spectrometer code ' + current_samp + ' and index ' + str(duplicates[n][k]))
            if k == 0:
                purest_samp = samp_purity[duplicates[n][0]]
                purest_index = duplicates[n][k]
                continue
            else:
                if len(purest_samp) > len(current_samp):
                    continue
                elif len(purest_samp) < len(current_samp):
                    purest_samp = samp_purity[duplicates[n][k]]
                    purest_index = duplicates[n][k]
                elif len(purest_samp) == len(current_samp):
                    current_sum = sum([ord(l) for l in current_samp]) #taken from https://stackoverflow.com/questions/28182454/multiple-characters-in-python-ord-function
                    purest_sum = sum(ord(m) for m in purest_samp)

                    print('(Current sum) The sum of ' + current_samp + ' is ' + str(current_sum))
                    print('(Pure sum) The sum of ' + purest_samp + ' is ' + str(purest_sum))

                    if current_sum > purest_sum:
                        continue
                    elif current_sum < purest_sum:
                        purest_samp = samp_purity[duplicates[n][k]]
                        purest_index = duplicates[n][k]
                    elif purest_sum == current_sum:
                        purest_samp = samp_purity[duplicates[n][k]]
                        purest_index = duplicates[n][k]
                        
        print('The purest sample has a spectrometer code of ' + str(samp_purity[purest_index]))
        purest_names.append(names[purest_index])
        purest_wavelengths.append(relevant_wavelengths[purest_index])
        purest_reflectances.append(reflectances[purest_index])
        purest_purities.append(samp_purity[purest_index])
    else:
        purest_names.append(names[duplicates[n][0]])
        purest_wavelengths.append(relevant_wavelengths[duplicates[n][0]])
        purest_reflectances.append(reflectances[duplicates[n][0]])
        purest_purities.append(samp_purity[duplicates[n][0]])
                    
                    
                    
        
for j in range(len(purest_names)):
    print(purest_names[j] + ' has indices of ' + str(list_duplicates_of(purest_names,purest_names[j])))


minerals = np.loadtxt('minerals.txt', unpack=True, dtype=str)

#Querying minerals
for w in range(len(minerals)):
    for x in range(len(purest_names)):
        if minerals[w] == purest_names[x]:
            same_name = (np.array(purest_names) == minerals[w])
            wave_out = np.array(purest_wavelengths)[same_name]
            refl_out = np.array(purest_reflectances)[same_name]
            
            list_wave_out = wave_out.tolist()
            list_refl_out = refl_out.tolist()
            
            print(list_wave_out)
            
            data = list(zip(wave_out[0], refl_out[0]))
            top = minerals[w] + '\n'
            top += 'wavelengths (microns), reflectance'
            file_name = minerals[w] + '.txt'
            np.savetxt(file_name, data, fmt='%s', delimiter = ', ', header=top)
            
            plt.figure(w)
            plt.plot(wave_out[0], refl_out[0])
            plt.xlabel('Wavelengths (microns)')
            plt.ylabel('Reflectance')
            plt.title(minerals[w] + ': Reflectance vs. Wavelength')
            plt.savefig(minerals[w] + '.png', dpi=150)
        