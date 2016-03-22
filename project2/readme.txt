# programming language use:
	python 2.7 and R

# code are divided into 3 folders as listed
	1. demographic for part A
		parser.py: parse suburb profile files and generate dictionary object
		geography.py: calculate suburb distance
		demographic.py: implement data preprocessing, similarity measures, dimension reduction.
		analysis.py: generate evaluation data and 2D plot
		visualisation.txt: include all funcitons used in R

		execution: python analysis.py

	2. economy and population for part A

		to get MSD plot just run econ.py or pop.py
		to show scatter plot of diversity vs. similarity, run plot.py
		  	economy test: uncomment line 30 and comment line 33
		  	population test: uncommnet line 33 and comment line 30

		to get linear relation of diversity vs. similarity using R by handling the data.txt generated from plot.py
			 execution in R: source("plot.R")

	3. Part B
		parser.py and crime.py for crime analysis
		diversityExtra.py and diversity.py for diveristy analysis

		just run them to get results.

	P.S. remember to put the project_data into every folder.



			

