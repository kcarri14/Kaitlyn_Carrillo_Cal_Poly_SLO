import sys
import nltk 
import math
import re
from nltk.corpus import wordnet as wn
#nltk.download('wordnet')
Synsets = wn.synsets('dog')

freq_cache = {}

def concept_freq(c1):
    #so we don't have to redo calculations
    if c1 in freq_cache:
        return freq_cache[c1]

    #counts total lemmas in the synset and adds one for smoothing
    total = sum(l.count() + 1 for l in c1.lemmas())

    #counts all the hyponyms lemma's
    for h in hyponym_list(c1):
        total += sum(l.count() + 1 for l in h.lemmas())

    #makes sure that we dont divide by 0 anywhere
    if total == 0:
        total = 1

    freq_cache[c1] = total
    return total


#finds the hypnoyms of all the hyponyms 
def hyponym_list(c1):
    seen = set()
    stack = list(c1.hyponyms())
    while stack:
        h = stack.pop()
        if h in seen:
            continue
        seen.add(h)
        stack.extend(h.hyponyms())
    return seen

#finds the total for the top most node
total_all = concept_freq(wn.synset("entity.n.01"))
#print(total_all)


def whole_thing(s):
    #combine everything together
    
    return -math.log(concept_freq(s) / total_all)


def lcs(c1, c2):
    #creates a dictionaru that maps all paths and max depths
    depth_map_c1 = {}
    #find all the paths
    paths = c1.hypernym_paths()
    for path in paths:
        for d, node in enumerate(path):
            if node not in depth_map_c1 or d > depth_map_c1[node]:
                depth_map_c1[node] = d
    
    depth_map_c2 = {}
    paths = c2.hypernym_paths()
    #print(paths)
    for path in paths:
        for d, node in enumerate(path):
            if node not in depth_map_c2:
                depth_map_c2[node] = d
    #print(depth_map_c1)
    #find the common ancestors between the two synsets
    common = set(depth_map_c1.keys()) & set(depth_map_c2.keys())

    #finds the ancestor closest to both the synsets
    best = None
    best_depth = 0
    for s in common:
        d = min(depth_map_c1[s], depth_map_c2[s])
        if d > best_depth:
            best_depth = d
            best = s
    return best, depth_map_c1, depth_map_c2

def tokenize(text):
    #eliminates puncuation
    return re.findall(r"[a-z]+", text.lower())

def gloss(s):
    #finds all definitions of itself, the hyponyms, the hypernyms
    def_list = [s]+ s.hyponyms() + s.hypernyms()
    tokens = []
    for d in def_list:
        tokens.extend(tokenize(d.definition()))
    return tokens

def overlap(a, b):
    best = (None, None, 0)
    max_n_grams = min(len(a), len(b))
    #starts with the biggest n-gram to find them in both lists
    for n in range(max_n_grams, 1, -1):
        #make dict of all n-grams and finds if there is a match 
        n_grams_dict = {}
        for i in range(len(a) - n + 1):
            n_grams = tuple(a[i:i+n])
            if n_grams not in n_grams_dict:
                n_grams_dict[n_grams] = []
            n_grams_dict[n_grams].append(i)

        for j in range(len(b) - n + 1):
            n_grams = tuple(b[j:j+n])
            if n_grams in n_grams_dict:
                i = n_grams_dict[n_grams][0]
                return (i, j, n)
    return best

def sim_path(c1, c2):
    lcs_node, depth_map_c1, depth_map_c2 = lcs(c1, c2)
    if lcs_node is None:
        return None
    d1 = depth_map_c1[c1]
    d2 = depth_map_c2[c2]
    depth_lcs = depth_map_c1[lcs_node]

    path_len = (d1 - depth_lcs) + (d2 - depth_lcs)
    if (path_len == 0):
        return 1
    else:
        return 1.0 / (path_len + 1)
    

def sim_resnik(c1, c2):
    lcs_res, _,_, = lcs(c1, c2)
    return whole_thing(lcs_res)

def sim_lin(c1, c2):
    lcs_lin, _,_, = lcs(c1, c2)
    return (2 * whole_thing(lcs_lin)) / ((whole_thing(c1)) + (whole_thing(c2)))

def sim_JC(c1, c2):
    lcs_JC, _,_, = lcs(c1, c2)
    return 1 /((2 * -(whole_thing(lcs_JC))) - (-(whole_thing(c1)) + -(whole_thing(c2))))

def sim_eLesk(c1, c2):
    #returns list of tokens
    segment1 = [gloss(c1)]
    segment2 = [gloss(c2)]
    score = 0
    
    while True:
        best = (None, None, None, None, 0)
        for index1, s1 in enumerate(segment1):
            if len(s1) < 1:
                continue
            for index2, s2 in enumerate(segment2):
                if len(s2) < 1:
                    continue
                #finds best overlap in the segments 
                i, j, n = overlap(s1, s2)
                if n > best[4]:
                    best = (index1, index2, i, j, n)
        #if there is no overlap, then break
        _, _, _, _, n = best
        if n == 0:
            break
        #removes the overlapping part so it is not counted again
        index1, index2, i, j, n = best
        s1 = segment1.pop(index1)
        s2 = segment2.pop(index2)
        #split the segments into lists so that the segments aren't overlapped 
        #with each other
        left1, right1 = s1[:i], s1[i+n:]
        left2, right2 = s2[:j], s2[j+n:]

        if left1:
            segment1.append(left1)
        if right1:
            segment1.append(right1)
        if left2:
            segment2.append(left2)
        if right2:
            segment2.append(right2)
        #add to the score
        score += n * n

    return score

def main():
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    if(arg1.count(".") == 2 and arg2.count(".") == 2):
        syn1 = wn.synset(arg1)
        syn2 = wn.synset(arg2)
        print(concept_freq(syn1) / total_all)
        print(f"Path Similarity: {sim_path(syn1, syn2):.3f}")
        print(f"Resnik Similarity: {sim_resnik(syn1, syn2):.3f}")
        print(f"Lin Similarity: {sim_lin(syn1, syn2):.3f}")
        print(f"JC Similarity: {sim_JC(syn1, syn2):.3f}")
        print(f"Extended Lesk Similarity: {sim_eLesk(syn1, syn2)}")
    else:
        arg1_syn = (wn.synsets(arg1, pos=wn.NOUN))
        arg2_syn = (wn.synsets(arg2, pos=wn.NOUN))
        if arg1_syn:
            arg1_syn = arg1_syn[0]
        else:
            print(f"No synset for this word: {arg1}")
            return
        
        if arg2_syn:
            arg2_syn = arg2_syn[0]
        else:
            print(f"No synset for this word: {arg2}")
            return
        
        print(f"Path Similarity: {sim_path(arg1_syn, arg2_syn):.3f}")
        print(f"Resnik Similarity: {sim_resnik(arg1_syn, arg2_syn):.3f}")
        print(f"Lin Similarity: {sim_lin(arg1_syn, arg2_syn):.3f}")
        print(f"JC Similarity: {sim_JC(arg1_syn, arg2_syn):.3f}")
        print(f"Extended Lesk Similarity: {sim_eLesk(arg1_syn, arg2_syn)}")

if __name__ == "__main__":
    main()

    