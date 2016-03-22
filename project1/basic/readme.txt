1. pair_set.py
	# generate all edges from train.txt, and store them in pair_set_whole.txt
	# given a proportion, generate pair_set_proportion.txt from pair_set_whole.txt
	# given a train_set ratio and a test_set ratio, generate pair_set_train.txt
	   and pair_set_test.txt from pair_set_proportion.txt
2. graph.py
	# generate two graphs
	#  graph_train.txt for extracting features for training
	#  graph_prop.txt for extracting features for testing

3. training_set_features.py
	# given pair_set_train.txt and graph_train.txt, extracting features to train_features.csv

4. test_set_features.py
	# given pair_set_test.txt and graph_test.txt, extracting features to test_features.csv

5. predict.py
	# given test_featres.csv and train_features.csv, generate predict.csv for test edges

P.S. 
	1. for test-public.txt, we get test_features.csv from whole graph constructed on pair_set_whole.
	2. node(src and dst) features: 
			number of follower, number of followee, ratio of follower and followee, pagerank
		edge(src->dst) features:
			cosine similarity, jaccard similarity





