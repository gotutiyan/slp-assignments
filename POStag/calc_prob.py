import argparse
from collections import defaultdict

def main(args):
    BOS = '<BOS>'
    word_pos_freq = dict() # {(word,pos): freq}
    bi_pos_freq = dict() # {}
    
    word_freq = defaultdict(int)
    pos_freq = defaultdict(int)
    with open(args.input) as fp:
        for line in fp:
            words = line.split()
            for word in words:
                word, pos = word.split('_')
                word_freq[word] += 1
                pos_freq[pos] += 1
                word_freq[BOS] += 1
                pos_freq[BOS] += 1
                word_pos_freq[(word, pos)] = word_pos_freq.get((word, pos), 0) + 1
            words = [BOS + '_' + BOS] + words
            for i in range(len(words)-1):
                word1, pos1 = words[i].split('_')
                word2, pos2 = words[i+1].split('_')
                bi_pos = (pos1, pos2)
                bi_pos_freq[bi_pos] = bi_pos_freq.get(bi_pos, 0) + 1
    word_pos_prob = dict()
    bi_pos_prob = dict()
    for word_pos, freq in word_pos_freq.items():
        # word_pos is tuple, (word, pos)
        prob = freq / word_freq[word_pos[0]]
        word_pos_prob[word_pos] = prob
    for bi_pos, freq in bi_pos_freq.items():
        prob = freq / pos_freq[bi_pos[0]]
        bi_pos_prob[bi_pos] = prob
    writer(word_pos_prob, args.word_pos_out)
    writer(bi_pos_prob, args.bi_pos_out)

    
def writer(d, file_path):
    with open(file_path, 'w') as fp:
        for k, v in d.items():
            # print(type(k[0]), type(k[1]), type(v))
            fp.write('\t'.join([k[0], k[1], str(v)]) + '\n')
    return        

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--bi_pos_out', default='bi_pos.tsv')
    parser.add_argument('--word_pos_out', default='word_pos.tsv')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_parser()
    main(args)