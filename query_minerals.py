#The purpose of this code is to query minerals that we want (we input this in minerals.txt, NOT case sensitive) + their information
#The program also plots the wavelength, reflectance data and returns a .txt file containing the data + info
#To run this file, make sure you are in the same directory as the file and type "python query_minerals.py" in the terminal window
#You can run this program as many times as you want

import numpy as np
import os
import re
import requests
from subprocess import call
import matplotlib.pyplot as plt
import sqlite3

minerals = np.loadtxt('minerals.txt', unpack=True, dtype=str, ndmin=1)

conn = sqlite3.connect('minspec.db')

c = conn.cursor()

for w in range(len(minerals)):
    minerals[w] = minerals[w].lower()
    minerals[w] = minerals[w].capitalize()
    c.execute("SELECT * FROM minerals WHERE name LIKE '" + minerals[w] + "'") #finding the mineral we want in our database
    myresult = c.fetchall()
    for result in myresult:
        wavelengths = result[4][1:-1].split(', ')

        for a in range(len(wavelengths)):
            wavelengths[a] = float(wavelengths[a])

        reflectances = result[5][1:-1].split(', ')
        for b in range(len(reflectances)):
            reflectances[b] = float(reflectances[b])

        #putting data into txt file
        data = list(zip(wavelengths, reflectances))
        top = result[0] + ', Chemical Formula: ' + str(result[1]) + '\n'
        top += 'Sample ID: ' + result[2] + '\n'
        top += 'wavelengths (microns), reflectance'
        file_name = result[0] + '_' + result[2] + '.txt'
        np.savetxt(file_name, data, fmt='%s', delimiter = ', ', header=top)

        #plotting data
        plt.plot(wavelengths, reflectances)
        plt.xlabel('Wavelengths (microns)')
        plt.ylabel('Reflectance')
        plt.title(result[0] + ', ' + result[2] + ': Reflectance vs. Wavelength')
        plt.savefig(result[0] + '_' + result[2] + '.png', dpi=150)

        plt.clf()
        plt.cla()

        
