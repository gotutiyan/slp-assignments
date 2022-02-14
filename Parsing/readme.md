# Introduction

This program for dependency parsing with shift-reduce method. Note that shift-reduce method required a stack (for shifted words) and a queue (for remain words) for after explanation. 

For feature, I used probability for commands (shift, reduce-R,L) with followings:

- Three words: first and second top word of the stack and most front word of a queue. 
- Three Part-Of-Speech: POSs corresponding first and second top word of the stack and most from word of a queue.

The probability corresponding each feature is computed by like `frequency / total` formula. In prediction, I chose the commands (shift, reduce-R,L) witch has highest probability of `P(commands | three words) * P(commands | three POS)`.


# Data Download
```bash
wget https://github.com/neubig/nlptutorial/raw/master/data/mstparser-en-train.dep
wget https://github.com/neubig/nlptutorial/raw/master/data/mstparser-en-test.dep
```

# Usage
```
python model.py --train mstparser-en-train.dep --test mstparser-en-test.dep
```

# Accuracy
0.05195085147661134

It seems something is wrong...
