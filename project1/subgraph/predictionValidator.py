FILENAME = "prediction-1000.csv"
l_score = []
import csv
i = 0
with open(FILENAME, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for iid,score in spamreader:
		if i == 0:
			i += 1
			continue
		l_score.append(float(score))
	more_50 = len(filter(lambda x: x >= 0.50,l_score))
	less_50 = len(filter(lambda x: x < 0.50,l_score))
	print "More than and equal 50 = %d" % (more_50)
	print "Less than 50 = %d" % (less_50)
	print "ratio more = %f%%, less = %f%%" %(float(more_50)/2000*100,float(less_50)/2000*100)
		