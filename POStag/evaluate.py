import argparse
import pos_tag

def loader(test_file):
    sentences = []
    labels = []
    with open(test_file) as fp:
        for line in fp:
            elems = line.split()
            sentence = []
            label = []
            for elem in elems:
                word, pos = elem.split('_')
                sentence.append(word)
                label.append(pos)
            sentences.append(sentence)
            labels.append(label)
    return sentences, labels

def main(args):
    BOS = '<BOS>'
    sentences, correct_labels = loader(args.input)
    bi2cost = {}
    pos2cost = {}
    pos_tag.loder('bi_pos.tsv', bi2cost)
    pos_tag.loder('word_pos.tsv', pos2cost)
    n_sum = 0
    n_correct = 0
    i = 0
    for sent, label in zip(sentences, correct_labels):
        i += 1
        # print(i)
        sent = [BOS] + sent
        try:
            ans = pos_tag.get_lattice(sent, bi2cost, pos2cost)
            pred = [elem[1] for elem in ans.get_greatest_path()]
            correct = [l1 == l2 for l1, l2 in zip(label, pred)]
            n_correct += sum(correct)
            n_sum += len(label)
        except IndexError:
            print(i)
            n_sum += len(label)
            pass
    print('Accuracy:', n_correct / n_sum)
        
        

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_parser()
    main(args)