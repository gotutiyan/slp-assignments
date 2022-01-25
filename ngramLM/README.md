# N-gram Language Model

### Data Download
```bash
wget https://github.com/neubig/nlptutorial/raw/master/data/wiki-en-train.word
wget https://github.com/neubig/nlptutorial/raw/master/data/wiki-en-test.word
```

### Usage
I confirmed it works with python 3.7.10.
```bash
python lm.py --train wiki-en-train.word --test wiki-en-test.word 
```
or, you can calculate an entropy score of a sentence.
```bash
python lm.py --train wiki-en-train.word --hand

# Then,
# Input: <please input a sentence freely>
# Entropy: An entropy of the input sentence.
```

### An Entropy Score of Test Dataset
```
Entropy on test data: 7.577128352216197
```

### Entropy of correct and incorrect sentence.

Example 1:
```
Input: I like math because it is funny .
Entropy: 3.627943873772967
Input: I like math because the dinner is very delicious.
Entropy: 4.347596565897724
```

Example 2:
```
Input: He is a doctor .
Entropy: 2.70805020110221
Input: He are a doctor .
Entropy: 3.0160655195602946
```

# Details

The function `get_ngram_freq()` is to extract n-grams.

The function `get_mgram_diff_context()` is to compute the number of contexts in which the n-1-gram appears.
