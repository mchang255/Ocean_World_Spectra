#The purpose of this program is to mix minerals, model the spectra of the mixtures, and unmix them (using multivariate curve resolution done by Dr. Laura Rodriguez). Currently, this program is tuned to using the files in salt_volumes, which models salt formation on Europa. salt_volumes provided by Dr. Marc Neveu 
#There are three input files: linear_mixing.txt, linear_mixing_param.txt, whole_library.txt
#linear_mixing.txt: specify the minerals you wish to mix in one column and the ID of the mineral sample that you wish to select in another. Separate the two columns with just a comma (,). We specify the ID because there could be multiple mineral samples that differ by grain size, temperature, etc.
#linear_mixing_param.txt: specify whether you wish to use the fractional or equilibrium mixtures. also specify whether you wish to use end-member spectra or guess percentages for initial estimates when unmixing minerals
#whole_library.txt: specify what minerals you would like to be as the end-member initial estimates for unmixing. Write the mineral in one column (I believe case-sensitive and spell correctly) and the ID in another, separate the two columns with a comma (,). As the name of the file implies, it should be the whole library aka whatever is in the mineral_data folder, but maybe there are some you wish to leave out.
#To run this file, make sure you have already queried the minerals you would like to use by first running query_minerals.py. Then type "python linear_mixing.py" into the terminal and press ENTER. Make sure you are the same directory as the file
#This program outputs the graphs of the combined spectra for each temperature of the mixture to a subfolder that has the mineral mixture in the name which is within a folder called "mixture_graphs" 
#This program also outputs (all to the same directory as the current program is in):
#_component_fractions.csv - the initial component fractions of each of the minerals (what was given in the salt_volumes file) (each row)
#_wavelength_convolved_spectra.csv - a matrix containing the wavelengths as the top row and all the linearly mixed mixtures every row beneath the first row
#_spectra_of_minerals.csv - the linearly interpolated spectra of the minerals (each row)
#_abundances.csv - what MCR believes is in the mixture and how much of it
#whole_library_reflectances.csv - interpolated data of the initial estimate end-member spectra to match the mineral mixture

import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.interpolate import interp1d

def check_if_equal(list_1, list_2): #from: https://thispointer.com/python-check-if-two-lists-are-equal-or-not-covers-both-ordered-unordered-lists/
    """ Check if both the lists are of same length and if yes then compare
    sorted versions of both the list to check if both of them are equal
    i.e. contain similar elements with same frequency. """
    if len(list_1) != len(list_2):
        return False
    return sorted(list_1) == sorted(list_2)

my_minerals,samp_id = np.loadtxt('linear_mixing.txt', delimiter=",", unpack=True, dtype=str, ndmin=1) #loading in minerals we want

#code structure taken from a past project done with another mentor. Code structure developed by a former intern
with open('linear_mixing_param.txt', 'r') as param: 
    lines = param.readlines()
    for line in lines:
        if line[:1] == '#':
            continue
        else:
            index = line.find('=')
            if 'freezing_sim_type' in line[:index]:
                freezing_sim_type = str(line[index+1:].strip())
            if 'spectra_or_frac' in line[:index]:
                spectra_or_frac = str(line[index+1:].strip())
                
minerals_dir = os.path.relpath(os.path.join(os.path.dirname(__file__),'mineral_data'))
all_minerals = os.listdir(minerals_dir)

num_minerals = len(my_minerals)

total_wave = ['Empty'] * num_minerals
total_refl = ['Empty'] * num_minerals

lists = [] #taken from: https://stackoverflow.com/questions/23999801/creating-multiple-lists
for k in range(num_minerals): #creates a bunch of empty lists to store the weight fractions of each mineral in each sample
    lists.append([])

salt_volumes_dir = os.path.relpath(os.path.join(os.path.dirname(__file__),'salt_volumes')) #needing our percentages for each mineral in mineral combination
all_salts = os.listdir(salt_volumes_dir)
all_salts.remove('.DS_Store')
all_salts.remove('.ipynb_checkpoints')

#selecting the file that we need for our minerals. This is accomplished by seeing what minerals are listed in the .csv file and checking if the minerals in that .csv are the same as the ones we listed in the input file
for a in range(len(all_salts)):
    if freezing_sim_type in all_salts[a]:
        file = os.path.join(salt_volumes_dir, all_salts[a])
        with open(file, 'r') as fi:
            lines = fi.readlines()
            for i in range(len(lines)):
                if i == 1:
                    minerals = lines[i].rstrip().split(',')[-num_minerals:]
                    if check_if_equal(my_minerals, minerals):
                        actual_minerals = minerals
                        file_we_want = file
    else:
        continue

lists = [] #taken from: https://stackoverflow.com/questions/23999801/creating-multiple-lists
for k in range(num_minerals):
    lists.append([])

#appending the weight fractions to our lists for each mineral. also appending temperatures
for_file = []
temps = []
with open(file_we_want, 'r') as fi:
    lines = fi.readlines()
    for i in range(len(lines)):
        if i == 0:
            continue
        elif i == 1:
            for e in range(num_minerals+1):
                if e == 0:
                    continue
                else:
                    lists[e-1].append(lines[i].rstrip().split(',')[-e])
        else:
            for_file.append(lines[i].rstrip().split(',')[-num_minerals:])
            temps.append(lines[i].rstrip().split(',')[0])
            for j in range(num_minerals+1):
                if j == 0:
                    continue
                else:
                    amount = float(lines[i].rstrip().split(',')[-j][:-1])
                    lists[j-1].append(amount/100)

order = []
#we want to make sure the order of the minerals in our weight fraction lists matches with the order of the minerals in the input file. if not, we will make the orders the same! then, we will be able to multiply the weight fractions with the appropriate mineral reflectances
for f in range(len(my_minerals)):
    index_we_want = [i for i, lst in enumerate(lists) if my_minerals[f] in lst][0] #https://stackoverflow.com/questions/25398259/finding-the-index-of-an-item-in-a-list-of-lists
    order.append(my_minerals[index_we_want])
    for j in range(len(all_minerals)):
        if '.txt' in all_minerals[j]:
            if samp_id[f] in all_minerals[j]:
                file = os.path.join(minerals_dir, all_minerals[j])
                wave, refl = np.loadtxt(file, delimiter="\t", unpack=True)
                total_wave[index_we_want] = wave
                total_refl[index_we_want] = refl


shortest_length = min(total_wave, key=len) #the mineral that has the least amount of wavelengths

#finding the max wavelength value for each mineral. out of the max wavelength values, which one is the lowest? we want the one that is the lowest because we will cut down the other arrays, so that the wavelength ranges roughly match across the board. we cut down the reflectance arrays accordingly
min_waves = []
for b in range(len(total_wave)):
    min_waves.append(np.max(total_wave[b]))
    
minnest = np.min(min_waves)
indices = np.where(min_waves == minnest)[0]

if len(indices) > 1:
    lengths = []
    for c in range(len(indices)):
        lengths.append(len(total_wave[indices[c]]))
    longest = np.max(lengths)
    indices_long = np.where(lengths == longest)[0]
    one_to_use = total_wave[indices_long]
else:
    one_to_use = total_wave[indices[0]]

new_filtered_refl = []
new_filtered_wave = []

# for b in range(len(my_minerals)):
#     print(my_minerals[b] + ' has a length of ' + str(len(total_wave[b])))

print(one_to_use)
#while we cut down the arrays to get the wavelength ranges in order, that doesn't mean the length of each of the arrays are the same. they need to be the same (and also have the same wavelength values)! we choose the mineral that has the least amount of wavelength values. 
for k in range(len(total_wave)):
    if np.array_equal(one_to_use,total_wave[k]):
        new_filtered_refl.append(total_refl[k])
        new_filtered_wave.append(total_wave[k])
    else:
        same_waves_BA = (total_wave[k] <= np.max(one_to_use))
        filtered_wave = total_wave[k][same_waves_BA]
        filtered_refl = total_refl[k][same_waves_BA]
        
        print(total_wave[k])
        print(filtered_wave)
        
        # print(my_minerals[k] + ' now has a length of ' + str(len(filtered_wave)))
        # print(filtered_wave)
        
        new_filtered_refl.append(filtered_refl)
        new_filtered_wave.append(filtered_wave)
        
        # f = interp1d(total_wave[k], total_refl[k])
        # new_refl.append(f(one_to_use))
        
shortest_length = min(new_filtered_wave, key=len)
new_refl = []

#print(new_filtered_wave)

#for the ranges that have more values than the shortest range, we interpolate them, so the shortest wavelength range can be applied. ta-da, now each of the reflectances have the same wavelengths associated with them
for r in range(len(new_filtered_wave)):
    if np.array_equal(shortest_length,new_filtered_wave[r]):
        new_refl.append(new_filtered_refl[r])
    else:
        print(new_filtered_wave[r])
        print(new_filtered_refl[r])
        f = interp1d(new_filtered_wave[r], new_filtered_refl[r])
        new_refl.append(f(shortest_length))

float_parts = []
for k in range(len(lists)):
    float_parts.append([])
    
parts_refl = []
for o in range(len(lists)):
    parts_refl.append([])
    
for z in range(len(lists)):
    for l in range(len(lists[z])):
        if l == 0:
            continue
        else:
            float_parts[z].append(float(lists[z][l]))

#multiplying each of the weight fractions with the correct mineral arrays
for m in range(len(float_parts)):
    for n in range(len(float_parts[m])):
        linear_mix_component = float_parts[m][n] * new_refl[m]
        parts_refl[m].append(linear_mix_component)
        

transposed_parts_refl = np.transpose(parts_refl,(1,0,2))

convolved_spectra = []

#adding up each sample to get a convolved spectra
for p in range(len(transposed_parts_refl)):
    convolved_spectra.append(sum(transposed_parts_refl[p]))
    
#saving to files
to_out = []
to_out.append(shortest_length)

for q in range(len(convolved_spectra)):
    to_out.append(convolved_spectra[q])

mineral_file = '_'.join(actual_minerals) #so that the order of the minerals lines with the percentages for the file name
mineral_file = mineral_file + '_' + freezing_sim_type

wavelength_convolved_spectra = mineral_file + '_wavelength_convolved_spectra.csv'
np.savetxt(wavelength_convolved_spectra, to_out, delimiter=", ") #wavelengths as the first row/columns, rest are the convolved spectra samples

percent_to_out = []
for s in range(len(float_parts)):
    percent_to_out.append(float_parts[s])

component_fractions = mineral_file + '_component_fractions.csv'
np.savetxt(component_fractions, percent_to_out, delimiter=", ") #weight fractions, each row represents one mineral

spectra_to_out = []
for t in range(len(new_refl)):
    spectra_to_out.append(new_refl[t])

spectra_of_minerals = mineral_file + '_spectra_of_minerals.csv'
np.savetxt(spectra_of_minerals, spectra_to_out, delimiter=", ") #endmember spectra, what the reflectances of each mineral look like before mixing/applying weight fractions. each row represents one mineral

#using the whole library for MCR to select what minerals it thinks are in the mixtures. This is to prevent 'cheating' - as in we already know what is in the mixture, so to reflect real life research, have the program guess what is in the mixture
whole_library = []
whole_library_minerals, whole_library_id = np.loadtxt('whole_library.txt', delimiter=",", dtype=str, unpack=True)
whole_library_names = []
for u in range(len(whole_library_id)):
    for v in range(len(all_minerals)):
        if '.txt' in all_minerals[v]:
            if whole_library_id[u] in all_minerals[v]:
                wavelength, reflectance = np.loadtxt(os.path.join(minerals_dir, all_minerals[v]), delimiter="\t", unpack=True)
                same_waves_BA = (wavelength <= np.max(shortest_length))
                filtered_wave = wavelength[same_waves_BA]
                filtered_refl = reflectance[same_waves_BA]
                
                same_waves_BA = (filtered_wave >= np.min(shortest_length))
                filtered_wave = filtered_wave[same_waves_BA]
                filtered_refl = filtered_refl[same_waves_BA]
                
                f = interp1d(filtered_wave, filtered_refl, fill_value="extrapolate") #some data may have values that lie outside of the interpolation range, so we need to extrapolate in order for the interpolation to work. Be aware that there may be a lot of errors if using extrapolation as the values don't vary in a particular pattern
                whole_library.append(f(shortest_length))
                whole_library_names.append(whole_library_minerals[u])

whole_library_to_out = []
for x in range(len(whole_library)):
    whole_library_to_out.append(whole_library[x])
whole_library_file = 'whole_library_reflectances.csv'
np.savetxt(whole_library_file, whole_library_to_out, delimiter=", ")

#graphing
mixtures_path = os.path.relpath(os.path.join(os.path.dirname(__file__),'mixture_graphs'))
os.makedirs(mixtures_path, exist_ok = True)

mixture_path = os.path.relpath(os.path.join(os.path.dirname(__file__),'mixture_graphs/' + mineral_file))
os.makedirs(mixture_path, exist_ok = True)

for z in range(len(convolved_spectra)):
    percentages = '_'.join(for_file[z])
    plt.plot(shortest_length, convolved_spectra[z])
    plt.title(mineral_file + ', ' + percentages + ', ' + temps[z] + ' K')
    plt.xlabel('Wavelength (microns)')
    plt.ylabel('Reflectance')
    
    img_name = mixture_path + '/' + mineral_file + '_' + percentages + '_' + temps[z] + 'K.png'
    plt.savefig(img_name, dpi=150)
    
    plt.clf()
    plt.cla()


import mcr #unmixing