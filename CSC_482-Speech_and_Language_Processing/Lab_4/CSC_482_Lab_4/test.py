import sys
import nltk
import spacy
from nltk import pos_tag
import re

nlp = spacy.load("en_core_web_sm")
quit_statements = {"q", "Q", "quit", "Quit", "QUIT"}
punctuation = {".", ",", ":", "``", "''", "-"}
e_quantifer_words = {"someone", "somebody",  "anybody", "anyone", "Someone", "Somebody", "Anybody", "Anyone"}
a_quantifer_words = { "everyone", "nobody", "everybody", "Nobody", "Everybody", "Everyone"}
run = 0
subject_list = []

def normalize(sentence):
    fol_sentence = []
    #tokenize
    word_tokens = nltk.word_tokenize(sentence)
            
    #pos tagging
    tagged_words = pos_tag(word_tokens)
    for words in tagged_words:
        if words[0] in e_quantifer_words: 
            fol_sentence.append("exists x.")
        if words[0] in a_quantifer_words:
            fol_sentence.append("all x.")

    return tagged_words, fol_sentence

def has_verb(tagged):
    return any(tag.startswith("VB") for _, tag in tagged)

def recursive_conjunctions(tagged_words):
    if not tagged_words:
            return ""
    tokens_lower = [w.lower() for w, _ in tagged_words]

    if tokens_lower[0] == "if":
        comma_i = tokens_lower.index(",")
        left = tagged_words[1:comma_i]          
        right = tagged_words[comma_i + 1:]       
        left_recurse = recursive_conjunctions(left)
        right_recurse = recursive_conjunctions(right)
        return f"({left_recurse} -> {right_recurse})"
    
    if "if" in tokens_lower:
        i = tokens_lower.index("if")
        left = tagged_words[:i]      
        right = tagged_words[i+1:]   
        if has_verb(left) and has_verb(right):
            left_recurse = recursive_conjunctions(left)
            right_recurse = recursive_conjunctions(right)
            return f"({right_recurse} -> {left_recurse})"

    for index, (words,_) in enumerate(tagged_words):
        w = words.lower()
        
        if w == "and" or w == "but":
            left = tagged_words[:index]
            right = tagged_words[index+1:]
            left_recurse = recursive_conjunctions(left)
            right_recurse = recursive_conjunctions(right)
            return f"({left_recurse} & {right_recurse})"
        if w == "or":
            left = tagged_words[:index]
            right = tagged_words[index+1:]
            left_recurse = recursive_conjunctions(left)
            right_recurse = recursive_conjunctions(right)
            return f"({left_recurse} | {right_recurse})"
    return translate_clause(tagged_words)

def translate_clause(words):
    
    for (word, _) in words:
        if word in punctuation:
            words.remove((word, _))
        else:
            continue
    words_str = " ".join(w[0] for w in words)
    doc = nlp(words_str)
    tokens = [
        {
            "position": token.i,
            "text": token.text,
            "pos": token.pos_,
            "dep": token.dep_,
            "head": token.head.i,
            "children": [child.i for child in token.children]
        }
        for token in doc
    ]

    root = None
    for token in tokens:
        if token['dep'] == 'ROOT':
            root = token
            break
    if not root:
        return ""
    
    subject = None
    for token in tokens:
        if token['dep'] == 'nsubj':
            subject = token["text"]
            subject_list.append(subject)
            break
        if token["text"] in e_quantifer_words or token["text"] in a_quantifer_words:
            subject = token["text"]
            subject_list.append(subject)
    if not root:
        return ""

    return get_predicate(tokens, root)

def get_predicate(tokens, root):
    predicate = root['text']
    subject = None
    obj = None

    # turn "is" into predicate
    if root['pos'] == 'AUX':
        for i in root['children']:
            child = tokens[i]
            if child['dep'] == 'nsubj':
                subject = child['text'] 
            elif child['dep'] == 'acomp' or child['dep'] == 'attr':
                predicate = child['text']

                for j in child['children']:
                    grandchild = tokens[j]
                    
                    if grandchild['dep'] == 'prep': 
                        for k in grandchild['children']:
                            if tokens[k]['dep'] == 'pobj':
                                obj = tokens[k]['text']
        if subject and obj:
            return f"{predicate}({subject}, {obj})"
        elif subject:
            return f"{predicate}({subject})"

    # normal verbs
    for i in root['children']:
        child = tokens[i]

        if child['dep'] == 'nsubj':
            subject = child['text']
        elif 'obj' in child['dep']:
            obj = child['text']
    
    if subject and obj:
        return f"{predicate}({subject}, {obj})"
    elif subject:
        return f"{predicate}({subject})"

    # default to include children??
    args = ", ".join(tokens[c]['text'] for c in root['children'])
    if args == "":
        return f"{predicate}({subject_list[run - 1]})"
    return f"{predicate}({args})" 


def fol(sentence):
    normalized_sentence, quantifers = normalize(sentence)
    conditional_sentence = recursive_conjunctions(normalized_sentence)
    if quantifers is not None:
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
    if (len(sys.argv) == 2):
        file_path = sys.argv[1]
        with open(file_path, "r") as f:
            files = f.read()

        sentence_tokens = nltk.sent_tokenize(files)
        for sentence in sentence_tokens:
            print(fol(sentence))
    else:
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
