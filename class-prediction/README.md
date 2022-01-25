# Class Prediction

### Data Download
```bash
wget https://github.com/neubig/nlptutorial/raw/master/data/titles-en-train.labeled
wget https://github.com/neubig/nlptutorial/raw/master/data/titles-en-test.labeled
```

### Usage
I confirmed it works with python 3.7.10.
```bash
python model.py --train titles-en-train.labeled --test titles-en-test.labeled
```

Output example:
```
Accuracy on train dataset: 0.9600460666194188
Accuracy on test dataset: 0.9263195182430038
```

### Details
I made model based on Naive Bayes.

This task can be regarded find class so that maximize P(c)P(d|c), where c and d correspond to a class and a document.
In addition, I computed P(d|c) as Π_{w in d} P(w|c), where w is a word in the document (d).

The program may be simple. The function of `calc_Pc()` is to compute P(c). Likewise, the function of `calc_Pwc()` is to compute P(w|c). Finally, the class of the document will be predict using `predict()` function.

If unknown word is appeared, I regared the word has occuring only once.

