import sys
import nltk
import spacy
from nltk import pos_tag
import re

nlp = spacy.load("en_core_web_lg")
quit_statements = {"q", "Q", "quit", "Quit", "QUIT"}
punctuation = {".", ",", ":", "``", "''", "-"}
e_quantifer_words = {"someone", "somebody",  "anybody", "anyone", "Someone", "Somebody", "Anybody", "Anyone", "Exactly"}
a_quantifer_words = { "everyone", "nobody", "everybody", "Nobody", "Everybody", "Everyone"}
self_list = {"himself", "herself", "themselves"}
run = 0
subject_list = []
last_event = None 


def normalize(sentence):
    fol_sentence = []
    sentence_list = []
    for words in sentence.split(" "):
        sentence_list.append(words)
    
    #tokenize
    word_tokens = nltk.word_tokenize(sentence)
    for index, words in enumerate(word_tokens):
        if words == "'s":
            word_tokens[index] = "is"
        if words == "n't":
            word_tokens[index] = "not"
        
    #pos tagging
    tagged_words = pos_tag(word_tokens)
    for words in tagged_words:
        if words[0] in e_quantifer_words: 
            fol_sentence.append("exists x.")
        if words[0] in a_quantifer_words:
            fol_sentence.append("all x.")

    return tagged_words, fol_sentence, sentence_list

# splits a sentence based on index
def split_sentence(tagged_words, index, sentence_list):
    left = tagged_words[:index]
    right = tagged_words[index+1:]
    left_has = has_verb(left)
    right_has = has_verb(right)
    if (not left_has) and right_has:
        right_recurse = recursive_conjunctions(right, sentence_list)
        left_recurse = recursive_conjunctions(left, sentence_list)
    else:
        left_recurse = recursive_conjunctions(left, sentence_list)
        right_recurse = recursive_conjunctions(right, sentence_list)

    return left_recurse, right_recurse

# returns if a token is a verb
def has_verb(tagged):
    return any(tag.startswith("VB") for _, tag in tagged)

def is_neg(tagged):
    any(pos in ("PROPN", "PRON", "NOUN") for _, pos in tagged)

def recursive_conjunctions(tagged_words, sentence_list):
    if not tagged_words:
            return ""
    tokens_lower = [w.lower() for w, _ in tagged_words]

    # "it is not the case that" special case
    if len(tokens_lower) >= 6 and tokens_lower[:6] == ["it", "is", "not", "the", "case", "that"]:
        rest = tagged_words[6:]
        rest_recurse = recursive_conjunctions(rest, sentence_list)
        return f"-({rest_recurse})"

    # simple implication 
    if tokens_lower[0] == "if":
        comma_i = tokens_lower.index(",")
        left = tagged_words[1:comma_i]          
        right = tagged_words[comma_i + 1:]       
        left_recurse = recursive_conjunctions(left, sentence_list)
        right_recurse = recursive_conjunctions(right, sentence_list)
        return f"({left_recurse} -> {right_recurse})"
    
    # complex implication
    if "if" in tokens_lower:
        i = tokens_lower.index("if")
        left = tagged_words[:i]      
        right = tagged_words[i+1:]   
        if has_verb(left) and has_verb(right):
            left_recurse = recursive_conjunctions(left, sentence_list)
            right_recurse = recursive_conjunctions(right, sentence_list)
            return f"({right_recurse} -> {left_recurse})"

    # conjunction / disjunction
    for index, (words,_) in enumerate(tagged_words):
        w = words.lower()
        
        if w == "and" or w == "but":
            left, right = split_sentence(tagged_words, index, sentence_list)
            return f"({left} & {right})"
        if w == "or":
            if tokens_lower[0] == "nobody":
                left = tagged_words[:index]
                right = tagged_words[index+1:]
                right_subject = any(pos in ("PROPN", "PRON", "NOUN") for _, pos in right)
                if not right_subject:
                    right = [("Nobody", "PRON")] + right

                left = recursive_conjunctions(left, sentence_list)
                right = recursive_conjunctions(right, sentence_list)
                return f"({left} & {right})"
            left, right = split_sentence(tagged_words, index, sentence_list)
            return f"({left} | {right})"
    return translate_clause(tagged_words, sentence_list)

# preprocessing
def translate_clause(words, sentence_list):
    for (word, _) in words:
        if word in punctuation:
            words.remove((word, _))
        else:
            continue
    words_str = " ".join(w[0] for w in words)

    # dependency parse
    doc = nlp(words_str)
    tokens = [
        {
            "position": token.i,
            "text": token.text,
            "lemma": token.lemma_,
            "pos": token.pos_,
            "dep": token.dep_,
            "children": [child.i for child in token.children]
        }
        for token in doc
    ]

    # check for root word, negation, and quantifiers
    root = None
    negated = False
    for token in tokens:
        if token['dep'] == 'ROOT':
            root = token
        if token['dep'] == 'neg' or token['text'] == 'nobody':
            negated = True       
        if token['dep'] == 'nsubj' and token['lemma'] != "it":
            subject = token["text"]
            subject_list.append(subject)
        if token["text"] in e_quantifer_words or token["text"] in a_quantifer_words:
            subject = token["text"]
            subject_list.append(subject)

    if not root:
        return ""

    return get_predicate(tokens, root, negated, sentence_list)

# given a sentence returns the predicate form
def get_predicate(tokens, root, negated, sentence_list):
    global last_event
    fol = ""
    predicate = root['text']
    subject = None
    obj = None
    prep = None

    #handles other than
    excluded = None
    for t in tokens:
        if t["lemma"] == "other":
            for c in t["children"]:
                if tokens[c]["dep"] == "prep" and tokens[c]["lemma"] == "than":
                    for g in tokens[c]["children"]:
                        if tokens[g]["dep"] == "pobj":
                            excluded = tokens[g]["text"]
    #handles excpet for
    except_name = None
    for t in tokens:
        if t["lemma"] == "except":
            for c in t["children"]:
                if tokens[c]["dep"] == "prep" and tokens[c]["lemma"] == "for":
                    for g in tokens[c]["children"]:
                        if tokens[g]["dep"] == "pobj":
                            except_name = tokens[g]["text"]

    #handles if only a name comes through the clause because of the recusrive call
    if (root["pos"] == "PROPN" or root["pos"] == "NOUN") and last_event and len(tokens) == 1:
        pred, last_obj = last_event
        subject = root["text"]
        if last_obj:
            fol = f"{pred}({subject}, {last_obj})"
        else:
            fol = f"{pred}({subject})"
        return '-' + fol if negated else fol
    
    # handle does types
    if root["lemma"] == "do" or root["lemma"] == "too":
        for i in root['children']:
            if tokens[i]['dep'] == 'nsubj':
                subject = tokens[i]['text']
        
        if last_event and subject:
            predicate, obj = last_event
            if obj:
                if obj and obj.lower() in self_list:
                    obj = subject
                fol = f"{predicate}({subject}, {obj})"
            else:
                fol = f"{predicate}({subject})"
            return '-' + fol if negated else fol
        
    # turn "is" into predicate
    if root['pos'] == 'AUX' and root['text'] != 'are':
        for i in root['children']:
            child = tokens[i]
            
            # for "it is not the case"
            if child['dep'] == 'ccomp':
                return get_predicate(tokens, child, negated, sentence_list)
            if child['dep'] == 'nsubj' and child['lemma'] != "it":
                subject = child['text']
            elif child['dep'] == 'acomp' or child['dep'] == 'attr' and child['text'] != 'case':
                predicate = child['text']

                for j in child['children']:
                    grandchild = tokens[j]
                    
                    if grandchild['dep'] == 'prep': 
                        for k in grandchild['children']:
                            if tokens[k]['dep'] == 'pobj':
                                obj = tokens[k]['text']

        if subject and obj:
            if obj and obj.lower() in self_list:
                    obj = subject
            fol = f"{predicate}({subject}, {obj})"
        elif subject:
            fol = f"{predicate}({subject})"
        return '-' + fol if negated else fol
            
    # normal verbs
    for i in root['children']:
        child = tokens[i]
        
        if child['dep'] == 'nsubj' and child['text'] != "it":
            subject = child['text']
        elif 'obj' in child['dep']:
            obj = child['text']
        elif child['dep'] == 'prep':
            prep = child['text']
            for k in child['children']:
                if tokens[k]['dep'] == 'pobj':
                    obj = tokens[k]['text']
    if prep:
        predicate = f"{predicate}_{prep}"
    if subject and obj:
        if obj and obj.lower() in self_list:
            obj = subject
        last_event = (predicate, obj)
        fol = f"{predicate}({subject}, {obj})"
        if excluded and obj in e_quantifer_words.union(a_quantifer_words):
            fol = f"({fol} & {obj} != {excluded})"
        if except_name and obj in a_quantifer_words:
            fol = f"({obj} != {except_name} -> {predicate}({subject}, {obj}))"
        if excluded and subject in a_quantifer_words and subject == "Nobody":
            fol = f"({subject} != {excluded} -> -{predicate}({subject}, {obj}))"
            return fol
    elif subject:
        last_event = (predicate, None)
        fol = f"{predicate}({subject})"
    else: 
        # default to include subject of the sentence
        args = ", ".join(tokens[c]['text'] for c in root['children'] if tokens[c]['text'] == 'nsubj')
        if args == "":
            for i in subject_list:
                for index, word in enumerate(sentence_list):
                    if word == i:
                        subject = sentence_list[index]
            if subject is None:
                fol = f"{predicate}()"
            else:
                fol = f"{predicate}({subject})"
        else:
            fol = f"{predicate}({args})" 
    return '-' + fol if negated else fol

# turn English sentence into first order logic
def fol(sentence):
    global last_event
    last_event = None
    normalized_sentence, quantifers, sentence_list  = normalize(sentence)
    conditional_sentence = recursive_conjunctions(normalized_sentence, sentence_list)
    # format quantifier information
    if(len(quantifers) != 0):
        sentence_list = re.findall(r'[A-Za-z_][A-Za-z0-9_]*|.', conditional_sentence)
        for index, words in enumerate(sentence_list):
            if words in e_quantifer_words or words in a_quantifer_words:
                sentence_list[index] = "x"
            else:
                continue
        sentence = "".join(sentence_list)
        return quantifers[0] + sentence
    return conditional_sentence

def main():
    # command line argument provided
    if (len(sys.argv) == 2):
        file_path = sys.argv[1]
        with open(file_path, "r") as f:
            files = f.read()

        sentence_tokens = nltk.sent_tokenize(files)
        for sentence in sentence_tokens:
            print(fol(sentence))
    else:
        # chatbot
        while(True):
            global run
            run += 1
            sentence = str(input("] "))
            if sentence in quit_statements:
                exit()
            else:
                
                print(fol(sentence))

    return


if __name__ == "__main__":
    main()