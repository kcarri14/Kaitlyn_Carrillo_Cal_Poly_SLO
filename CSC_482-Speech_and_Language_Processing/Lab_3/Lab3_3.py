# import nltk
# nltk.download('treebank')
from nltk.corpus import treebank
import re

verbs = {"VB", "VBD", "VBG", "VBN", "VBP", "VBZ"}
nouns = {"NN", "NNS", "NNP", "NNPS"}

punctuation = {".", ",", ":", "``", "''", "-LRB-", "-RRB-", "$", "#", "-NONE-", "-"}
nonterminals = set()

def choose_head(parent_label, child_label):
#find rightmost nonterminal
    def rightmost(cands):
        for i in range(len(child_label) - 1, -1, -1):
            if child_label[i] in cands:
                return i
        return None
#find leftmost nonterminal
    def leftmost(cands):
        for i in range(len(child_label)):
            if child_label[i] in cands:
                return i
        return None
  #look for rightmost noun  
    if parent_label == "NP":
        idx = rightmost(nouns | {"NP"})
        if idx is not None:
            return idx
        return len(child_label) - 1
#look for leftmost verb
    if parent_label == "VP":
        idx = leftmost(verbs | {"VP"})
        if idx is not None:
            return idx
        return 0
#look for rightmost preposition
    if parent_label == "PP":
        idx = rightmost({"NP"})
        if idx is not None:
            return idx
        return len(child_label) - 1
#look for the rightmost verb
    if parent_label in {"S", "SBAR"}:
        idx = leftmost({"VP"})
        if idx is not None:
            return idx
        return 0
#look for the rightmost adjective
    if parent_label == "ADJP":
        idx = rightmost({"JJ", "JJR", "JJS", "ADJP"})
        if idx is not None:
            return idx
#look for the rightmost adverb
    if parent_label == "ADVP":
        idx = rightmost({"RB", "RBR", "RBS", "ADVP"})
        if idx is not None:
            return idx

    return len(child_label) - 1

def count_trees(fileids):
    rule_count = {}
    ls_count = {}
    new_lhs_rules = re.compile(r'[-^_=|_$].*') 

    trees = treebank.parsed_sents(fileids)
#helper function to recurisvely call and find head for the sentences
    def process(node):
        if isinstance(node, str):
            return ("", node)
        #base case
        if len(node) == 1 and isinstance(node[0], str):
            #replace all puncutation with PUNC
            if node.label() in punctuation:
                tag = "PUNC"
            else:
                tag = new_lhs_rules.sub('',node.label())
            word = node[0]
            return (tag, word)
        #replace all puncutation with PUNC
        if node.label() in punctuation:
            tag = "PUNC"
        else:
            parent = new_lhs_rules.sub('',node.label())

        if parent == "":
            leaves = [w for w in node.leaves() if isinstance(w, str)]
            return ("", leaves[-1] if leaves else "UNK")
        
        #recursively go through attached the head word to the nonterminal
        child_info = []
        child_labels = []
        for ch in node:
            if isinstance(ch, str):
                continue
            c_lbl, c_head = process(ch)
            if c_lbl == "":
                continue
            child_info.append((c_lbl, c_head))
            child_labels.append(c_lbl)
        if not child_info:
            leaves = [w for w in node.leaves() if isinstance(w, str)]
            return (parent, leaves[-1] if leaves else "UNK")
        #find head 
        head_idx = choose_head(parent, child_labels)
        head_word = child_info[head_idx][1]
        #if the head is puncutation find a different word
        if head_word in punctuation:
            non_punct = [i for i, (_, hw) in enumerate(child_info) if hw not in punctuation]
            if non_punct:
                if parent == "NP":
                    head_idx = max(non_punct)          
                elif parent in {"VP", "S", "SBAR"}:
                    head_idx = min(non_punct)          
                else:
                    head_idx = max(non_punct)          
                head_word = child_info[head_idx][1]

        lhs_sym = f"{parent}-{head_word}"
        rhs_syms = []
        for (c_lbl, c_head) in child_info:
            rhs_syms.append(f"{c_lbl}-{c_head}")

        if len(rhs_syms) > 0:
            rhs_tup = tuple(rhs_syms)
            key = (lhs_sym, rhs_tup)
            rule_count[key] = rule_count.get(key, 0) + 1
            ls_count[lhs_sym] = ls_count.get(lhs_sym, 0) + 1
        return (parent, head_word)
    #print(trees)
    for tree in trees:
        process(tree)
    
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