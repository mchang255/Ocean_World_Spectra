Read-me file to run the algorithm of Lapotre et al. (2017), JGR: Planets, doi: 10.1002/2016JE005248


*****************************
Pasadena, 06/13/2017
Updated at Stanford, 05/20/2022
Mathieu Lapotre
mlapotre@stanford.edu
*****************************


- Input files: 
(1) spectral data; as an example here, "O33E33A33.txt" (lab mixture of 33% olivine, 33% enstatite, 33% anorthite, D = 45-75 microns). This file needs to contain a column of wavelengths in meters, and a column of reflectance or SSA values.
(2) endmember optical constants; as an example here, you can find three files: "olivine.txt", etc. Those should contain a column of wavelengths (in meters), a column of n values, and a column of k values.

- load_data.m
This routine loads the data. THIS IS THE ONLY ROUTINE THAT REQUIRES USER INPUT/MODIFICATION. Input parameters/lines of code to adapt are highlighted in comments. As an example, the load_data routine is currently written for 3 mineral endmembers. To add more endmembers, simply add more values into the vectors that require input (e.g., density vector) as well as more endmember optical constant files.

Note: There is an option to use SSA spectra instead of reflectance spectra; to do so, set "R1_vs_SSA0" to "0" in load_data.m. 

- Main routine: MAIN.m
This routine runs the algorithm. 

- Outputs: 
	(1) MAP model (displayed in matlab Command Window), 
	(2) A matrix containing all accepted models (grain sizes and mass abundances) as "Results.mat", 
	(3)"BestFit_and_Residuals.jpg": Shows the data and MAP model.
	(4)"Distributions_and_Correlations.jpg": Shows distributions of accepted model parameters and their correlations. In the distribution plots, solid vertical lines indicate the MAP model, dashed lines the 68% confidence interval, and dotted lines the 95% confidence interval.


*****************************
Please cite:
Lapotre, M.G.A., B.L. Ehlmann, and S.E. Minson (2017), A probabilistic approach to remote compositional analysis of planetary surfaces, JGR: Planets, doi: 10.1002/2016JE005248.
*****************************
