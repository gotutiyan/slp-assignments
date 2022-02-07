from math import log
class Word:
    def __init__(self, pos, name):
        self.pos = pos
        self.name = name

    def get_value(self):
        return (self.name, self.pos)
    
    def __eq__(self, other):
        return (self.pos == other.pos 
                and self.name == other.name)


class Node:
    def __init__(self, cost, word_pos, word_name, parents):
        self.cost = cost
        self.word = Word(word_pos, word_name)
        self.parents = parents

    def get_greatest_path(self):
        ret=[]
        if self.word.name == '<BOS>':
            ret=[]
        else:
            if self.word.name == '<EOS>':
                ret = self.parents[0].get_greatest_path()+[]
            else:
                ret=self.parents[0].get_greatest_path()+[self.word.get_value()]
        return ret


def loder(tsv_file, dict_name):
    with open(tsv_file)as f:
        for line in f:
            line = line.split('\t')
            if dict_name.get(line[0]) == None:
                dict_name[line[0]] = {}
            dict_name[line[0]].update({line[1]:float(line[2])})

def get_lattice(sentence, bi2cost, pos2cost):
    queue = []
    appeared = {}
    init = Node(0, '<BOS>', '<BOS>', [])
    appeared[(init.word.get_value(), 0)] = init
    queue.append(init)
    for i in range(1, len(sentence)):
        length = len(queue)
        for j in range(length):
            now_node = queue[0]
            del queue[0]
            if sentence[i] in pos2cost.keys():
                for next_pos in pos2cost[sentence[i]]:
                    # print(next_pos)
                    # print(now_node.word.pos)
                    # print(bi2cost[now_node.word.pos])
                    if bi2cost.get(now_node.word.pos, {}).get(next_pos) is not None:
                        next_cost = now_node.cost \
                                    + log(bi2cost[now_node.word.pos][next_pos]) \
                                    + log(pos2cost[sentence[i]][next_pos])
                        next_node = Node(next_cost, next_pos, sentence[i], [now_node])
                        if (next_node.word.get_value(), i) in appeared:
                            node = appeared[(next_node.word.get_value(), i)]
                            node.parents.append((next_node.parents[0]))
                            node.cost = max(node.cost, next_node.cost)
                            node.parents.sort(key=lambda parent : parent.cost, reverse=True)
                        else:
                            appeared.update({(next_node.word.get_value(), i) : next_node})
                            queue.append(next_node)
            else:
                for next_pos in bi2cost[now_node.word.pos]:
                    # print(next_pos)
                    # print(now_node.word.pos)
                    # print(bi2cost[now_node.word.pos])
                    if bi2cost.get(now_node.word.pos, {}).get(next_pos) is not None:
                        next_cost = now_node.cost \
                                    + log(bi2cost[now_node.word.pos][next_pos])
                        next_node = Node(next_cost, next_pos, sentence[i], [now_node])
                        if (next_node.word.get_value(), i) in appeared:
                            node = appeared[(next_node.word.get_value(), i)]
                            node.parents.append((next_node.parents[0]))
                            node.cost = max(node.cost, next_node.cost)
                            node.parents.sort(key=lambda parent : parent.cost, reverse=True)
                        else:
                            appeared.update({(next_node.word.get_value(), i) : next_node})
                            queue.append(next_node)

    return queue[0]
    
def main():
    bi2cost = {}
    pos2cost = {}
    loder('bi_pos.tsv', bi2cost)
    loder('word_pos.tsv', pos2cost)
    with open("sample.txt")as f:
        for sentence in f:
            sentence = sentence.split()
            sentence = ['<BOS>'] + sentence
            ans = get_lattice(sentence, bi2cost, pos2cost)
            print(ans.cost, ans.get_greatest_path(), sep="\n")

if __name__ == '__main__':
    main()