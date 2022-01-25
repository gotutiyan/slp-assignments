import argparse
import math
from collections import Counter

def load_file(train_file: str):
    labels = []
    sentences = []
    with open(train_file) as fp:
        for line in fp:
            line = line.strip()
            label, sentence = line.split('\t')
            sentence = sentence.split()
            labels.append(label)
            sentences.append(sentence)
    return labels, sentences

def calc_Pc(labels: list):
    '''
    Pc: A probability of the class
    '''
    labels_freq = {}
    Pc = {}
    for label in labels:
        labels_freq[label] = labels_freq.get(label, 0) + 1
    for label, freq in labels_freq.items():
        Pc[label] = freq / len(labels)
    return labels_freq, Pc

def calc_Pwc(labels: list, sentences: list, labels_freq: dict):
    '''
    Pwc: Probability of the word in the class
    '''
    freq_wc = dict() # {class: {word: freq}}
    for label, sentence in zip(labels, sentences):
        for token in set(sentence):
            freq_wc[label] = freq_wc.get(label, dict())
            freq_wc[label][token] = freq_wc[label].get(token, 0) + 1
    Pwc = dict()
    for label in freq_wc:
        Pwc[label] = dict()
        N_label = labels_freq[label]
        for token in freq_wc[label]:
            Pwc[label][token] = freq_wc[label][token] / N_label
    return freq_wc, Pwc

def predict(sentences: list, Pc: dict, Pwc: dict, labels_freq: dict):
    labels = ['-1', '1']
    predictions = []
    for sentence in sentences:
        log_probs = []
        for label in labels:
            sum_log_prob = math.log(Pc[label])
            for token in sentence:
                if token in Pwc[label]: # known word
                    sum_log_prob += math.log(Pwc[label][token])
                else: # An unknown word is considered to have occurred once.
                    sum_log_prob += math.log(1 / (labels_freq[label] + len(Pwc[label])))
            log_probs.append(sum_log_prob)
        pred_idx = argmax(log_probs)
        predictions.append(labels[pred_idx])
    return predictions

def calc_acc(preds: list, golds: list):
    acc = 0
    for pred, gold in zip(preds, golds):
        if pred == gold:
            acc += 1
    return acc / len(preds)

def argmax(elems: list):
    max_elem = max(elems)
    for i, elem in enumerate(elems):
        if max_elem == elem:
            return i

def main(args):
    # train
    train_labels, train_sentences = load_file(args.train)
    labels_freq, Pc = calc_Pc(train_labels)
    freq_wc, Pwc = calc_Pwc(train_labels, train_sentences, labels_freq)
    train_preds = predict(train_sentences, Pc, Pwc, labels_freq)
    print('Accuracy on train dataset:', calc_acc(train_preds, train_labels))
    # predict
    if args.test:
        test_labels, test_sentences = load_file(args.test)
        test_preds = predict(test_sentences, Pc, Pwc, labels_freq)
        print('Accuracy on test dataset:', calc_acc(test_preds, test_labels))

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', required=True)
    parser.add_argument('--test')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_parser()
    main(args)