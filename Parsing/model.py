import argparse
import numpy as np
from math import log

class Word:
    def __init__(self, self_id, word, pos, parent_id, dep):
        self.id = self_id
        self.word = word
        self.pos = pos
        self.parent_id = parent_id
        self.dep = dep

class Tree:
    def __init__(self, word):
        self.word = word
        self.parent_id = -1
        self.dep_with_parent = str
        self.l_children = []
        self.r_children = []

    def get_tree(self):
        result = []
        if len(self.l_children) > 0:
            for l_elem in self.l_children:
                result += l_elem.get_tree()
        # result += [(self.word.word, self.word.parent_id)] # Note it is Tree.parent_id, not Word.parent_id
        result += [(self.word.id, self.parent_id)] # Note it is Tree.parent_id, not Word.parent_id
        if len(self.r_children) > 0:
            for r_elem in self.r_children:
                result += r_elem.get_tree()
        return result

def load_file(input_file):
    sentences = []
    data_list = open(input_file).read().split('\n\n')
    for data in data_list:
        sentence = []
        for line in data.split('\n'):
            if len(line) == 0: continue
            self_id, word1, word2, pos1, pos2, _, parent_id, dep = line.split('\t')
            word_instance = Word(self_id, word1, pos1, parent_id, dep)
            sentence.append(word_instance)
        sentences.append(sentence)
    return sentences

def update_freq(key_word, key_pos, command_prob_word, command_prob_pos, command):
    command_prob_word[key_word] = command_prob_word.get(key_word, dict())
    command_prob_word[key_word][command] = command_prob_word[key_word].get(command, 0) + 1
    command_prob_pos[key_pos] = command_prob_pos.get(key_pos, dict())
    command_prob_pos[key_pos][command] = command_prob_pos[key_pos].get(command, 0) + 1

def train(sentences):
    command_prob_word = dict()
    command_prob_pos = dict()
    n_sum_commands = 0
    for sentence in sentences:
        if sentence == []: continue
        root = Tree(
            Word(-1, 'ROOT', 'ROOT', -1, 'ROOT')
        )
        stack = [root, Tree(sentence[0])]
        remain_words = sentence[1:]
        while len(remain_words) > 0:
            n_sum_commands += 1
            key_word = (stack[-2].word.word, stack[-1].word.word, remain_words[0].word)
            key_pos = (stack[-2].word.pos, stack[-1].word.pos, remain_words[0].pos)
            # reduce-L
            if stack[-2].word.parent_id == stack[-1].word.id:
                update_freq(key_word, key_pos, command_prob_word, command_prob_pos, 'L')
                stack[-1].l_children.append(stack[-2])
                del stack[-2]
            # reduce-R
            elif stack[-1].word.parent_id == stack[-2].word.id:
                update_freq(key_word, key_pos, command_prob_word, command_prob_pos, 'R')
                stack[-2].r_children.append(stack[-1])
                del stack[-1]
            # shift
            else:
                update_freq(key_word, key_pos, command_prob_word, command_prob_pos, 'S')
                stack.append(Tree(remain_words[0]))
                del remain_words[0]
    for key in command_prob_word:
        for command in ['L', 'R', 'S']:
            try:
                command_prob_word[key][command] /= n_sum_commands
            except:
                # unknown command has one occurrence
                command_prob_word[key][command] = 1 / n_sum_commands
    for key in command_prob_pos:
        for command in ['L', 'R', 'S']:
            try:
                command_prob_pos[key][command] /= n_sum_commands
            except:
                # unknown command has one occurrence
                command_prob_pos[key][command] = 1 / n_sum_commands
    return command_prob_word, command_prob_pos
                
def prediction(sentences, command_prob_word, command_prob_pos):
    n_correct = 0
    n_sum = 0
    for sentence in sentences:
        if sentence == []: continue
        root = Tree(
            Word(-1, 'ROOT', 'ROOT', -1, 'ROOT')
        )
        stack = [root, Tree(sentence[0])] # list of Tree instance
        remain_words = sentence[1:] # list of Word instance
        golds = [(word.id, word.parent_id) for word in sentence] # Word.parent_id object
        while len(remain_words) > 0:
            # determine commands (shift or reduce-R or reduce-L) by greedy...
            command = None
            if len(stack) < 2: # shift
                stack.append(Tree(remain_words[0]))
                del remain_words[0]
                continue
            key_word = (stack[-2].word.word, stack[-1].word.word, remain_words[0].word)
            key_pos = (stack[-2].word.pos, stack[-1].word.pos, remain_words[0].pos)
            if key_word not in command_prob_word:
                # Unknown candidate's command is shift
                command_prob_word[key_word] = dict()
                command_prob_word[key_word]['L'] = 1e-6
                command_prob_word[key_word]['R'] = 1e-6
                command_prob_word[key_word]['S'] = 1e-6
            if key_pos not in command_prob_pos:
                # Unknown candidate's command is shift
                command_prob_pos[key_pos] = dict()
                command_prob_pos[key_pos]['L'] = 1e-6
                command_prob_pos[key_pos]['R'] = 1e-6
                command_prob_pos[key_pos]['S'] = 1e-6
            else:
                min_prob = 1e9
                for command_cand in ['L', 'R', 'S']:
                    cand_prob = log(command_prob_word[key_word][command_cand])\
                                + log(command_prob_pos[key_pos][command_cand])
                    if min_prob > cand_prob:
                        min_prob = cand_prob
                        command = command_cand
            # print(command)
            # apply the command
            if command == 'L': # reduce-L
                stack[-1].l_children.append(stack[-2])
                stack[-2].parent_id = stack[-1].word.id
                del stack[-2]
            elif command == 'R': # reduce-R
                stack[-2].r_children.append(stack[-1])
                stack[-1].parent_id = stack[-2].word.id
                del stack[-1]
            else: # shift
                stack.append(Tree(remain_words[0]))
                del remain_words[0]
        while len(stack) > 1:
            # reduce-R
            stack[-2].r_children.append(stack[-1])
            stack[-1].parent_id = stack[-2].word.id
            del stack[-1]
        preds = stack[0].get_tree()
        # print('pred:', preds)
        # print('gold:', golds)
        # print()
        n_sum += len(golds)
        n_correct += evaluate(preds, golds)
        # n_correct += sum(np.array(result[1:]) == np.array(parent_id_ans))
    return n_correct / n_sum

def evaluate(preds, golds):
    # results and preds: list of (id, parent_id) object
    n_correct = 0
    for gold in golds:
        for pred in preds:
            if gold[0] == pred[0] and gold[1] == pred[1]:
                n_correct += 1
    return n_correct
                
                

def main(args):
    sentences_train = load_file(args.train)
    command_prob_word, command_prob_pos = train(sentences_train)
    sentences_test = load_file(args.test)
    acc = prediction(sentences_test, command_prob_word, command_prob_pos)
    print(acc)
    

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', required=True)
    parser.add_argument('--test', required=True)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_parser()
    main(args)

