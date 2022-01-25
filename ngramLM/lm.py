
import argparse
import math

def load_file(train_file: str) -> list:
    sentences = []
    with open(train_file) as fp:
        for sent in fp:
            sent = sent.strip()
            tokens = sent.split()
            sentences.append(tokens)
    return sentences

def get_ngram_freq(sentences: list, n: int) -> dict:
    ngram_freq = {}
    for sentence in sentences:
        for i in range(len(sentence)-n+1):
            ngram = tuple(sentence[i:i+n])
            ngram_freq[ngram] = ngram_freq.get(ngram, 0) + 1
    return ngram_freq

def get_mgram_diff_context(sentences, n):
    mgram_diff_context_set = {} # {mgram: set()}
    for sentence in sentences:
        for i in range(len(sentence)-n+1):
            ngram = tuple(sentence[i:i+n])
            mgram = ngram[:-1]
            mgram_diff_context_set[mgram] = \
                mgram_diff_context_set.get(mgram, set())
            mgram_diff_context_set[mgram].add(ngram[-1])
    mgram_diff_context_freq = {}
    for mgram, value in mgram_diff_context_set.items():
        mgram_diff_context_freq[mgram] = len(value)
    return mgram_diff_context_freq

def calc_ngram_prob(ngram_freq: dict, d: float, mgram_diff_context_freq:dict) -> dict:
    ngram_prob = {}
    for ngram, freq in ngram_freq.items():
        mgram = ngram[:-1]
        try:
            ngram_prob[ngram] = (freq - d) / (mgram_diff_context_freq[mgram])
        except:
            ngram_prob[ngram] = (1 - d) / (len(ngram_freq))
    return ngram_prob

def calc_entropy(sentences: list, ngram_prob: dict, n: int) -> float:
    log_prob = 0
    ngram_freq = get_ngram_freq(sentences, n)
    N = len(ngram_freq)
    for ngram, freq in ngram_freq.items():
        try:
            log_prob += math.log(ngram_prob[ngram]) * freq
        except KeyError:
            log_prob += math.log(1 / N) * freq
    return -1/N * log_prob


def main(args):
    train_sentences = load_file(args.train_file)
    ngram_freq = get_ngram_freq(train_sentences, args.n)
    # mgram_freq = get_ngram_freq(train_sentences, args.n-1)
    mgram_diff_context = get_mgram_diff_context(train_sentences, args.n) 
    ngram_prob = calc_ngram_prob(ngram_freq, args.d, mgram_diff_context)
    if args.hand:
        while True:
            sentence = input('Input: ')
            if sentence in ['exit', 'quit']:
                break
            entropy = calc_entropy([sentence], ngram_prob, args.n)
            print('Entropy:',entropy)
    elif args.test_file:
        test_sentences = load_file(args.test_file)
        entropy = calc_entropy(test_sentences, ngram_prob, args.n)
        print('Entropy on test data:', entropy)
    else:
        print('Error: Please set --hand or --test_file <file_path>')
    return
    

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n', type=int, default=2)
    parser.add_argument('--train_file', required=True)
    parser.add_argument('--test_file')
    parser.add_argument('--laplace', type=int, default=1)
    parser.add_argument('--d', type=float, default=0.5)
    parser.add_argument('--hand', action='store_true')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_parser()
    main(args)