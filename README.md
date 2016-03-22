# statistical_machine_learning

######################## project 1
# Pairwise relationships are prevalent in real life. For example, friendships between people, communication links between computers and pairwise similarity of cars. A way to represent a group of relationships is using networks, which consists of a set of nodes and edges. The entities in question are represented as the nodes and the pairwise relations as the edges.
# In real data, often there are missing edges between nodes. This can be due to a bug or deficiency in the data collection process, the lack of resources to collect all pairwise relations or simply there is uncertainty about those relationships. Analysis performed on incomplete networks with missing edges can bias the final output, e.g., if we want to find the shortest path between two cities in a road network, but we are missing information of major highways between these cities, then no algorithm will not be able to find this actual shortest path.
# Furthermore, we might want to predict if an edge will form between two nodes in the future. For example, in a disease transmission network, if health authorities determine a high likelihood of a transmission edge forming between an infected and uninfected person, then the authorities might wish to vaccinate the uninfected person.
# Hence, being able to predict and correct for missing edges is an important task.

# In this project, first learning from a training network and then trying to predict whether edges exist among test node pairs.



######################## project 2

# Australian suburbs are geographic subdivisions mainly used for addressing purposes. Greater Melbourne is subdivided into several hundreds of suburbs, home to 4.4 million people spread over 10,000 km2. There is a large diversity across suburbs that originates from geographic and historical reasons. Suburbs differ in a number of aspects ranging from land area to population demographics. Understanding this diversity, learning from it and using it to the advantage of community presents a major challenge for the government.
# The first step in addressing this challenge is collecting statistical information about suburbs, and this has been performed on a regular basis. Moreover, Victorian government supports the policy of open data, whereby accumulated statistical profiles are available to public free of charge. In particular, Department of Health and Human Services (DHHS) has released statistical profiles for suburbs. The task of understanding similarities and differences between the profiles now becomes a data analytic challenge.
# In this project, you will take on the challenge, addressing the problem in two parts. The first part will be driven by a specific research question, while the second part will be an exploratory open-ended analysis. You will perform unsupervised data analysis using statistical suburb profiles available from DHHS. You will work in a team of 3 people and, as a team, you will submit a report about your findings.