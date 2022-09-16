#The purpose of this program is to unmix mineral compositions using multivariate curve resolution. It is contained in another program (linear_mixing.py). For the time being, please run that program to get the results of the this program
#All credit for the MCR coding goes to Dr. Laura Rodriguez of the Origins and Habitability Lab at Jet Propulsion Laboratory
#This program, as part of linear_mixing.py, specifically outputs the abundances of what MCR believes to be in the input mineral mixture

import numpy as np
import pandas as pd
from scipy.optimize import nnls
import matplotlib.pyplot as plt
import os

from __main__ import *

def normalize(spec, use_max = False, axis = -1):
    if use_max:
        return spec / spec.max(axis = axis, keepdims = True)
    return spec / np.linalg.norm(spec, ord = 2, axis = axis, keepdims = True)

#to easily plot components
#spec = vector of intensities to plot
#wl = vector of wavelengths measured
def plot_spec(spec, wl, xticks = False):
    fig, ax = plt.subplots(1, 1, figsize = (8, 3))
    ax.plot(wl, spec)
    ax.set_xlabel('Wavelength (nm)')
    ax.set_ylabel('Intensity')
    if not xticks:
        ax.get_xaxis().set_visible(False)
    fig.tight_layout()
    plt.show()
    
def plot_image(img):
    if img.ndim == 3:
        img = img.mean(axis = 2)
    fig, ax = plt.subplots(1, 1, figsize = (4, 4))
    ax.imshow(img, cmap = 'viridis')
    ax.axis('off')
    fig.tight_layout()
    plt.show()
    
def MCR(img, num_components, C_est = None, S_est = None, max_iter = 500, mse_thresh = 1e-10,
        nonnegative = True, fixed_comp = None, normalize = False, verbose = False, seed = 45):
    '''
    Performs MCR-ALS on a hyperspectral image. Inputs are img (rows x columns x bands) and
    number of components to extract. C_est (num_pixels x num_components OR rows x columns x 
    num_components) and S_est (num_components x bands) are initial estimates for C and S (can 
    only provide one). If neither are provided, initializes S using SVD. Params max_iter and 
    mse_thresh are stopping criteria, and nonnegative forces a non-negativity constraint. Can 
    also provide abundances or components to fix by passing a list to fixed_comp with the 
    indices of the components that should not be updated. 
    
    Modified from PyMCR: https://github.com/usnistgov/pyMCR/blob/master/pymcr/mcr.py
    '''
    # reshape to 2D if needed
    if img.ndim == 3:
        i, j, k = img.shape
        pix = i * j
        img_r = img.reshape((pix, k))
    else:
        pix, k = img.shape
        img_r = img.copy()
    reps = 0
    mse_new = 1.
    np.random.seed(seed)
    
    # Initialization - use starting estimates if provided, otherwise generate initial components
    if C_est is not None and S_est is not None:
        raise ValueError('Can only provide starting estimate for C or S, not both')
    elif C_est is not None:
        #assert C_est.shape == (i, j, num_components) or C_est.shape == (pix, num_components), 'C_est is improper shape'
        start_C = False
        if C_est.ndim == 3 or C_est.shape[0] != pix:
            C_est = C_est.reshape((pix, -1))
        #C_old = C_est.copy()
        comp_est = C_est.shape[1]
        C_old = np.random.rand(pix, num_components)
        C_old[:,:comp_est] = C_est
        S_old = np.zeros((num_components, k))
    elif S_est is not None:
        #assert S_est.shape == (num_components, k), 'S_est is improper shape'
        start_C = True
        #S_old = S_est.copy()
        if S_est.shape[-1] != k:
            S_est = S_est.reshape(-1, k)
        comp_est = S_est.shape[0]
        S_old = np.random.rand(num_components, k)
        S_old[:comp_est,:] = S_est
        C_old = np.zeros((pix, num_components))
    else:
        # if no initial estimates provided come up with initial estimate for S using SVD
        start_C = True
        comp_est = 0
        C_old = np.zeros((pix, num_components))
        U, S, V = np.linalg.svd(img_r, full_matrices = False)
        S_old = V[:num_components]
        if np.sum(S_old) < 0:  # invert if needed
            S_old *= -1
        
    S_new = np.zeros(S_old.shape)
    C_new = np.zeros(C_old.shape)
    if nonnegative:  # make starting values positive
        C_old = np.abs(C_old)
        S_old = np.abs(S_old)
    if fixed_comp == 'all':  # only some component estimates provided above and want to keep all of them
        assert comp_est < num_components, 'provided component estimates n >= num_components'
        fixed_comp = list(range(comp_est))
    
    # Alternating Least Squares loop - continues until sufficient convergence or max_iter reached
    while (mse_new > mse_thresh and reps < max_iter):
        if start_C:  # need to estimate C first
            # fix S and solve for new C
            if nonnegative:
                for m in range(pix):
                    C_new[m,:] = nnls(S_old.T, img_r[m,:])[0]
            else:  # standard least squares
                C_new = np.linalg.pinv(S_old.T).dot(img_r.T).T
                
            # normalize the abundances to sum to 1 if requested
            if normalize:
                C_new /= C_new.sum(axis = 1, keepdims = True)
                
            # now fix C (newly-optimized) and use it to solve for new S
            if nonnegative:
                for m in range(k):
                    S_new[:,m] = nnls(C_new, img_r[:,m])[0]
            else:  # standard least squares
                S_new = np.linalg.pinv(C_new).dot(img_r)
                
            # restore any fixed S components
            if fixed_comp:
                S_new[fixed_comp,:] = S_old[fixed_comp,:]
        
        else:  # need to estimate S first
            # fix C and solve for new S
            if nonnegative:
                for m in range(k):
                    S_new[:,m] = nnls(C_old, img_r[:,m])[0]
            else:  # standard least squares
                S_new = np.linalg.pinv(C_old).dot(img_r)
                
            # now fix S (newly-optimized) and use it to solve for new C
            if nonnegative:
                for m in range(pix):
                    C_new[m,:] = nnls(S_new.T, img_r[m,:])[0]
            else:  # standard least squares
                C_new = np.linalg.pinv(S_new.T).dot(img_r.T).T
                
            # normalize the abundances to sum to 1 if requested
            if normalize:
                C_new /= C_new.sum(axis = 1, keepdims = True)
                
            # restore any fixed C components
            if fixed_comp:
                C_new[:,fixed_comp] = C_old[:,fixed_comp]
        
        # calculate new D and residuals (MSE) to check for convergence
        D_new = np.dot(C_new, S_new)
        mse_new = np.mean((D_new - img_r)**2)
        reps += 1
        if verbose:
            print('Iteration: {}, MSE: {}'.format(reps, mse_new.round(7)))
            
        # transfer newly-optimized loadings for next round
        C_old = C_new.copy()
        S_old = S_new.copy()
        
    if verbose:
        print('\nTotal iterations: {}'.format(reps))
        print('Final MSE: {}'.format(mse_new.round(7)))
    
    # sort the components
    # A = np.diag(np.dot(S_new, S_new.T))
    # order = np.argsort(A)[::-1]  # largest to smallest
    # S_new = S_new[order]
    # C_new = C_new[:,order]
    
    if img.ndim == 3:
        return C_new.reshape((i, j, num_components)), S_new
    return C_new, S_new

#Here we run the MCR code
#change to number of components 
#data_np is your data
#S_est = pure spectra estimate (here set to none since I had no starting guess)
#C_est = estimate of abundances (here set to none since I had no starting guess)
#fixed_comp = if you give it starting guesses, this is the indices for which to keep fixed (here none since I had no constraints)
#components = intensity values for every component. To plot, you also need the wavelengths (defined as wl in the function below)
#the MSE = mean square error; lower = better

#loading fractions of components for each sample
fractions_path = os.path.relpath(os.path.join(os.path.dirname(__file__), component_fractions))
fractions_data = np.loadtxt(fractions_path, delimiter=", ")
data_np_fractions = np.array(fractions_data)

#loading spectra of each component
component_path = os.path.relpath(os.path.join(os.path.dirname(__file__), whole_library_file))
component_data = np.loadtxt(component_path, delimiter=", ")
data_np_component = np.array(component_data)

#this assumes your data is as follows: rows = samples; column names = wavelengths
#first read in your data and save as object (here let's say data)
path = os.path.relpath(os.path.join(os.path.dirname(__file__),wavelength_convolved_spectra)) #path to your csv w/all your spectra
data = pd.read_csv(path) #reads in your data
#data_np = normalize(data_np) #you want to nomralize your spectra before MCR (see functions at the top for how I did this)
data_np = np.array(data) #changes your data to an array
wl = list(data.columns) #grabs the wavelengths (assuming column names = wavelengths)

#in MCR the first argument will be data_np

#deciding whether to use spectra or percentages for the initial estimate
if spectra_or_frac == 'spectra':
    abundances, components = MCR(data_np, num_components = len(data_np_component), nonnegative = True, verbose = True, max_iter = 50, normalize = True, C_est =None, S_est =data_np_component, fixed_comp = None) 
elif spectra_or_frac == 'frac':
    abundances, components = MCR(data_np, num_components = len(my_minerals), nonnegative = True, verbose = True, max_iter = 50, normalize = True, C_est =data_np_fractions, S_est =None, fixed_comp = None) 

for a in range(len(whole_library_names)):
    if a == 0:
        top = whole_library_names[a]
    else:
        top += ',' + whole_library_names[a]
    

#outputting estimates to file
abundances_file = mineral_file + '_abundances.csv'
np.savetxt(abundances_file, abundances, header=top, delimiter =",", fmt='%2.3f',comments='')