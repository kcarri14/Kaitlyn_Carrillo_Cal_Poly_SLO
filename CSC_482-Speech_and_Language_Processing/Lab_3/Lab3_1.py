# import nltk
# nltk.download('treebank')
from nltk.corpus import treebank

nonterminals = set()
num_phrase_rules = set()
num_lexicon_rules = set()


def count_trees(fileids):
    rule_count = {}
    ls_count = {}
    #get trees from treebank
    trees = treebank.parsed_sents(fileids)
    #for each production in the tree
    for tree in trees:
        #print(tree)
        for prod in tree.productions():
            #get the left hand side
            lhs = str(prod.lhs())
            #get the right hand side
            rhs = tuple(str(sym) for sym in prod.rhs())  

            #add them to the rule counts dict to get the total number
            #of them in all the trees
            key = (lhs, rhs)
            rule_count[key] = rule_count.get(key, 0) + 1
            #add the left hand sides to a dict to get the total number
            #of them to use for the probabilites
            ls_count[lhs] = ls_count.get(lhs, 0) + 1

    
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
    print(f"Nonterminals: {len(nonterminals)}")
    print(f"Total Rules: {len(rules)}")
    return 

if __name__ == "__main__":
    main()