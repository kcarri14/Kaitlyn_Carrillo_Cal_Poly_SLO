import nltk 
nltk.download('gutenberg')
from nltk.corpus import gutenberg
import random
import sys
import re

bos = '<S>'
eos = "</S>"
bop = "<P>"

def choices(freq):
    word = random.choice(list(freq.keys()))
    return word

def fix_tokens(tokens):
    #print(tokens)
    real_sentences = []
    for t in tokens:
        if t == bos or t == eos or t == bop:
            continue
        if t in {".", ",", "!", "?", ":", ";"}:
            real_sentences[-1] = real_sentences[-1] + t
        elif t.startswith("'") and len(t) > 1:
            real_sentences[-1] = real_sentences[-1] + t
        else:
            real_sentences.append(" " + t)
    s = "".join(real_sentences)
    s = re.sub(r"\s+([.,!?;:])", r"\1", s)
    s = s.strip()
    if s:
        s = s[0].upper() + s[1:]
    return s

def generate_trigram_sentence(trigram, first_sentence):
    sentence = []
    restarts = 0
    if first_sentence:
        w1, w2 = bop, bos
    else:
        w1, w2 = bos, bos
    
    while w2 not in {".","!","?"}:
        if (w1,w2) not in trigram:
            restarts += 1
            if restarts >= 3:
                break
            w1, w2 = bos, bos
            continue
        next_word = choices(trigram[(w1, w2)])
        if next_word == eos:
            break
        sentence.append(next_word)
        if next_word in {".","!","?"} and len(sentence) >= 6:
            break
        w1, w2 = w2, next_word
    return fix_tokens(sentence)

def generate_paragraph(model):
    n_sent = random.randint(2, 5)
    sents = []
    for i in range(n_sent):
        #print(i)
        sents.append(generate_trigram_sentence(model, (i == 0)))
    return " ".join(sents)

def is_verse_number(tokens, i):
    return (
        i + 2 < len(tokens)
        and tokens[i].isdigit()
        and tokens[i + 1] == ":"
        and tokens[i + 2].isdigit()
    )

def get_verse_number(tokens, i):
    return tokens[i] + ":" + tokens[i + 2]

def main():
        list_trigrams = {}
       
        results = list(gutenberg.words("bible-kjv.txt"))
        #print(results)
        verses = []
        i = 0
        n = len(results)
        verse_number_list = []
        
        while i< n:
            if is_verse_number(results, i):
                verse_number = get_verse_number(results, i)
                i += 3  
                verse_tokens = []
                #this is my word, sentence, and paragraph tokenizer becauase i didn't know if we could use sent_tokenize()
                #since it uses the punkt nltk
                while i < n and not is_verse_number(results, i):
                    verse_tokens.append(results[i].lower())
                    i += 1
                if verse_tokens:
                    verses.append((verse_number, verse_tokens))
                    verse_number_list.append(verse_number)

            else: 
                i+=1
                
        #print(verses)
        for n, v in verses:
            sentences = []
            current = []
            for t in v:
                if t in {"(", ")", "[", "]", "{", "}", "``", "''", '"', "'", "--", "—"}:
                    continue
                current.append(t)
                if t in {".", "!", "?"}:
                    sentences.append(current)
                    current = []
            if current:
                sentences.append(current)
            
            first_sentence = True

            words = []
            #print(sentences)
            for s in sentences:
                for t in s:
                    if t not in {"(", ")", "[", "]", "{", "}", "``", "''", '"', "'", "--", "—"}:
                        words.append(t)
                
                if first_sentence:
                    seq = [bop, bos, bos] + s + [eos]
                    #print(seq)
                    first_sentence = False
                else:
                    seq = [bos, bos] + s + [eos]
            
            
                for i in range(len(seq) - 2):
                    w1 = seq[i]
                    w2 = seq[i+1]
                    w3 = seq[i+2]
                    if (w1,w2) not in list_trigrams:
                        list_trigrams[(w1,w2)] = {}
                    list_trigrams[(w1,w2)][w3] = list_trigrams[(w1,w2)].get(w3, 0) + 1
                #print(list_trigrams)
        
        for k in range(1,4):
            print(f"Paragraph {k}")
            verse_number = random.choice(verse_number_list)
            print(f"{verse_number} {generate_paragraph(list_trigrams)}")
            print("")


if __name__ == "__main__":
    main()
