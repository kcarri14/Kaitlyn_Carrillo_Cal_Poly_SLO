# import nltk
# nltk.download('treebank')
from nltk.corpus import treebank
import re

nonterminals = set()
punctuation = {".", ",", ":", "``", "''", "-LRB-", "-RRB-", "$", "#", "-NONE-", "-"}

def count_trees(fileids):
    rule_count = {}
    ls_count = {}
    new_lhs_rules = re.compile(r'[-^_=|_].*') 

    trees = treebank.parsed_sents(fileids)
    #print(trees)
    for tree in trees:
        for prod in tree.productions():
            if prod.is_lexical():
                continue
            lhs = str(prod.lhs())
            new_lhs = new_lhs_rules.sub('', lhs)
            if (new_lhs == ''):
                continue
            #print(new_lhs)
            rhs = []
            bad_rhs = False
            for sym in prod.rhs():
                sym_str = str(sym)
                if sym_str in punctuation:
                    sym_str = "PUNC"
                    continue
                sym_vanilla = new_lhs_rules.sub('', sym_str)
                if sym_vanilla == '':
                    bad_rhs = True
                    break
                rhs.append(sym_vanilla)

            if bad_rhs:
                continue

            rhs_tup = tuple(rhs)
            if not rhs_tup:
                continue

            key = (new_lhs, rhs_tup)
            rule_count[key] = rule_count.get(key, 0) + 1
            ls_count[new_lhs] = ls_count.get(new_lhs, 0) + 1

    for (lhs, rhs) in rule_count:
        nonterminals.add(lhs)
    return rule_count, ls_count

def compute_probablities(rules, lhs_count):
    pcfg = []
    #go through each rule count in rules and find the probability   
    #of each one by dividing the count by the total number on the lhs
    for (lhs, rhs), count in rules.items():
        prob = count / lhs_count[lhs]
        #print(prob)
        pcfg.append((lhs, rhs, prob))
    return pcfg

#output to a file
def output_pcfg(pcfg):
    with open("pcfg.txt", 'w') as f:
        for (lhs, rhs, prob) in pcfg:
            rhs_str = " ".join(rhs)
            f.write(f"{lhs} -> {rhs_str} [{prob:.4f}]\n")
    return
            

def main():
    fileids = treebank.fileids()
    rules, lhs = count_trees(fileids)
    #print(lhs)
    pcfg = compute_probablities(rules, lhs)
    output_pcfg(pcfg)
    print(f"Nonterminal: {len(nonterminals)}")
    print(f"Total Rules: {len(rules)}")
    return 

if __name__ == "__main__":
    main()