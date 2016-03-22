FILENAME = "prediction-1000.csv"
PREDICTION = "normalized-1000.csv"
predict_file = open(PREDICTION,"w") 
print >> predict_file, "Id,Prediction"



import csv
i = 0
with open(FILENAME, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for iid,score in spamreader:
		if i == 0:
			i += 1
			continue
		print >> predict_file,"%s,%f" % (iid,float(score)+0.2)