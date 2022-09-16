#The purpose of this program is to calculate the absolute percentage difference between the original proportions (data in the salt_volumes folder) and calculated proportions (data in the abundances.csv files)
#There is one input file: percent_error_minerals.txt
#percent_error_minerals.txt: just type of the names of the minerals in a mixture you wish to see the percentage difference of. One mineral per row, and for the time-being, it is case sensitive and make sure you spell correctly. The very last row, however, should either have eq or frac to denote which type of mixture you would like to unmix - fractional or equilibrium
#To run this program, make sure you have the abundances file ready (run linear_mixing.py first). Type "python percent_error_mixtures.py" in the terminal and press ENTER. Make sure you are in the same directory as the file
#There is a graph with the suffix "percentage_differences.png" that shows the absolute percentage difference for each of the minerals between the predicted and actual proportions in mixture specified. It is outputted to a subfolder that has the mineral mixture in the name which is within a folder called "mixture_graphs" 

import numpy as np
import matplotlib.pyplot as plt
import os
import math

def check_if_equal(list_1, list_2): #from: https://thispointer.com/python-check-if-two-lists-are-equal-or-not-covers-both-ordered-unordered-lists/
    """ Check if both the lists are of same length and if yes then compare
    sorted versions of both the list to check if both of them are equal
    i.e. contain similar elements with same frequency. """
    if len(list_1) != len(list_2):
        return False
    return sorted(list_1) == sorted(list_2)


minerals = np.loadtxt('percent_error_minerals.txt', dtype=str, unpack=True)
eq_or_frac = minerals[-1]
minerals = minerals[:-1]

minerals_dir = os.path.relpath(os.path.dirname(__file__))
all_minerals = os.listdir(minerals_dir)

type_abundance = eq_or_frac + '_abundances.csv'
for a in range(len(all_minerals)):
    if type_abundance in all_minerals[a]:
        list_of_minerals = all_minerals[a].split('_')[:-2]
        if check_if_equal(minerals,list_of_minerals):
            file = all_minerals[a]
            
# with open(file, 'r') as fi:
#     lines = fi.readlines()
#     for b in range(len(lines)):
#         if b == 0:
#             library_minerals = lines[b].split(',')

mcr_data = [] #taken from: https://stackoverflow.com/questions/23999801/creating-multiple-lists
for b in range(len(minerals)):
    mcr_data.append([])

data = np.loadtxt(file, delimiter=",", dtype=str)

for c in range(len(minerals)):
    index = list(data[0]).index(minerals[c])
    for d in range(len(data)):
        mcr_data[c].append(data[d][index])
        
original_data = [] #taken from: https://stackoverflow.com/questions/23999801/creating-multiple-lists
for e in range(len(minerals)):
    original_data.append([])
    
salt_volumes_dir = os.path.relpath(os.path.join(os.path.dirname(__file__),'salt_volumes')) #needing our percentages for each mineral in mineral combination
all_salts = os.listdir(salt_volumes_dir)
all_salts.remove('.DS_Store')
all_salts.remove('.ipynb_checkpoints')

#selecting the file that we need for our minerals. This is accomplished by seeing what minerals are listed in the .csv file and checking if the minerals in that .csv are the same as the ones we listed in the input file
for a in range(len(all_salts)):
    if eq_or_frac in all_salts[a]:
        file_name = os.path.join(salt_volumes_dir, all_salts[a])
        with open(file_name, 'r') as fi:
            lines = fi.readlines()
            for i in range(len(lines)):
                if i == 1:
                    real_minerals = lines[i].rstrip().split(',')[-len(minerals):]
                    if check_if_equal(minerals, real_minerals):
                        actual_minerals = real_minerals
                        file_we_want = file_name
    else:
        continue

#appending the weight fractions to our lists for each mineral. also appending temperatures
for_file = []
temps = []
with open(file_we_want, 'r') as fi:
    lines = fi.readlines()
    for i in range(len(lines)):
        if i == 0:
            continue
        elif i == 1:
            for e in range(len(minerals)+1):
                if e == 0:
                    continue
                else:
                    original_data[e-1].append(lines[i].rstrip().split(',')[-e])
        else:
            for_file.append(lines[i].rstrip().split(',')[-len(minerals):])
            temps.append(lines[i].rstrip().split(',')[0])
            for j in range(len(minerals)+1):
                if j == 0:
                    continue
                else:
                    amount = float(lines[i].rstrip().split(',')[-j][:-1])
                    original_data[j-1].append(amount/100)


percent_error_data = [] #taken from: https://stackoverflow.com/questions/23999801/creating-multiple-lists
for e in range(len(minerals)):
    percent_error_data.append([])
    
for f in range(len(minerals)):
    index_we_want_mcr = [i for i, lst in enumerate(mcr_data) if minerals[f] in lst][0] 
    index_we_want_original = [i for i, lst in enumerate(original_data) if minerals[f] in lst][0]
    for g in range(len(mcr_data[index_we_want_mcr])):
        if g == 0:
            percent_error_data[f].append(mcr_data[index_we_want_mcr][g])
        else:
            float_mcr = float(mcr_data[index_we_want_mcr][g])
            float_original = float(original_data[index_we_want_original][g])
            print('Float MCR is: ' + str(float_mcr))
            print('Float original is: ' + str(float_original))
            percent_error = (abs(float_mcr - float_original)) * 100
            print('Percent difference is: ' + str(percent_error))
            percent_error_data[f].append(percent_error)

fig = plt.figure(figsize=(12,12))

for h in range(len(temps)):
    temps[h] = float(temps[h])
    
for g in range(len(percent_error_data)):
    sqr_root = math.ceil(np.sqrt(len(percent_error_data)))
    ax = fig.add_subplot(sqr_root,sqr_root,g+1)
    ax.plot(temps, percent_error_data[g][1:])
    ax.set_title(percent_error_data[g][0] + ': MCR vs. Original')
    ax.set_xlabel('Temperature (K)')
    ax.set_ylabel('Absolute Percentage Difference (%)')

mineral_file = '_'.join(actual_minerals) #so that the order of the minerals lines with the percentages for the file name
mineral_file = mineral_file + '_' + eq_or_frac

mixture_path = os.path.relpath(os.path.join(os.path.dirname(__file__),'mixture_graphs/' + mineral_file))
os.makedirs(mixture_path, exist_ok = True)

fig_name = mixture_path + '/' + mineral_file + '_percentage_differences.png'
plt.savefig(fig_name, dpi=150)

