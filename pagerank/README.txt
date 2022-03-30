Instructions for Running pageRank.py:

1. Make sure you have networkx installed on your machine.

2. The command looks something like "python3 pageRank.py <filepath> <directed> [big]"

   <filepath> is a path to a file. <directed> is either "T" or "F" (True or False) 
   specifiying if the file is directed or undirected. [big] is either "T" or "F" like
   <directed>. This parameter is only if you are testing the SNAP sets. It won't print 
   the full output of the snap sets (it's alot) and it calls a special readFile function.
   Some files can be run as either directed or undirected. You could test to see how 
   if affects output if you want.
   
Example runs for a couple of files:

# big file example
python3 pageRank.py ./data/amazon0505.txt T T

# undirected small file
python3 pageRank.py ./data/lesmis.csv F

# directed small file
python3 pageRank.py ./data/karateDir.csv