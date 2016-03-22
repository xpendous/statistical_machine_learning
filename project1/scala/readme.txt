Introduction:
We have two strategies of implementation for this project. The first one is using python together with scikit and networkx to fast establish the enrire development enviroment. The second solution is spark with graphx to generate features from entire graph.

Spark solution:
The scala code generate_features.sacala can be executed by copying and pasting each line of the definition and the entire function seperately to spark-shell to run. With this solution, we can generate the features from the entire graph in a reasonable time. With this code, the time for generating the features for 10% of trainig set data from the entire graph is less than one hour.

Exectable Environment:
1. Google cloud platform with computing resources of four ssd disk of 375 G, 16 core-cpu, and 104G memeory
2. Spark 1.4.1
3. Graphx(Integrated in Spark installation package)
4. Scala(Integrated in Spark installation package)

Input:
pair set file

Output:
Generate features by edge pair set