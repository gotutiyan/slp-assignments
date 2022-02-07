# POS tagging

I used Viterbi algorithm. My model consider two kind of probabilites: (i) bi-gram of POS, (ii) POS a word can take. The program first construct lattice (Edges are related probability(i), Nodes are related probability(ii)), then find highest probability path by Viterbi algorithm.

# Data Download
```bash
wget https://github.com/neubig/nlptutorial/raw/master/data/wiki-en-train.norm_pos
wget https://github.com/neubig/nlptutorial/raw/master/data/wiki-en-test.norm_pos
```

# Usage
```bash
python calc_prob.py --input wiki-en-train.norm_pos
python evaluate.py --input wiki-en-test.norm_pos 
```

# Accuracy

0.834319526627219

Note: The program doesn't work in the line 1, 3, 11, 51, 77, 93, 106, 141, 156 sentences. These sentence were treated that all prediction is incorrect. It is not known why the program does not work with these sentences.

