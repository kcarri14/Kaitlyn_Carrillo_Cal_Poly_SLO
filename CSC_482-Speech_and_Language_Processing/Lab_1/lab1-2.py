import nltk 
from nltk.corpus import gutenberg
import random
import re

books = ["austen-emma.txt", "austen-persuasion.txt", "austen-sense.txt"]

bos = "<s>"
eos = "</s>"

def choices(freq):
    word = random.choice(list(freq.keys()))
    return word

def fix_tokens(tokens):
    real_sentences = []
    for t in tokens:
        if not real_sentences:
            real_sentences.append(t)
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

def generate_trigram_sentence(trigram):
    sentence = []
    w1, w2 = bos, bos
    for i in range(30):
        next_word = choices(trigram[(w1, w2)])
        if next_word == eos:
            break
        sentence.append(next_word)
        if next_word in {".", "!", "?"}:
            break
        w1, w2 = w2, next_word
    if sentence and sentence[-1] not in {".", "!", "?"}:
        sentence.append(".")
    return fix_tokens(sentence)

def generate_bigram_sentence(trigram):
    sentence = []
    w1 = bos
    print(trigram[w1])
    for i in range(30):
        next_word = choices(trigram[w1])
        if next_word == eos:
            break
        sentence.append(next_word)
        if next_word in {".", "!", "?"}:
            break
        w1=next_word
    if sentence and sentence[-1] not in {".", "!", "?"}:
        sentence.append(".")
    return fix_tokens(sentence)

def merge_markers(toks):
    out = []
    i = 0
    while i < len(toks):
        if i + 2 < len(toks) and toks[i] == "<" and toks[i+2] == ">":
            mid = toks[i+1]
            if mid == "s":
                out.append("<s>")
                i += 3
                continue
            if mid == "/s":
                out.append("</s>")
                i += 3
                continue
        out.append(toks[i])
        i += 1
    return out

def main():
        list_trigrams = {}
        list_bigrams = {}

        for i in books:
            results = gutenberg.raw(i)
            results = results.lower()
            results = re.sub(r"\[[^\]]*\]", " ", results)
            results = re.sub(r"\bchapter\s+[ivxlcdm0-9]+\b", " ", results)
            results = re.sub(r"\s+", " ", results).strip()
            sentences = re.split(r"(?<=[.!?])\s+", results)
            words = []
            #print(sentences[0])
            for s in sentences:
                tokens = nltk.word_tokenize(s.lower())
                tokens = [bos] + tokens + [eos]
                for t in tokens:
                    if t not in {"(", ")", "[", "]", "{", "}", "``", "''", '"', "'", "--", "—"}:
                        t = t.lower()
                        words.append(t)
            
           
            for j in range(len(words) - 1):
                w1 = words[j]
                w2 = words[j+1]
                list_bigrams.setdefault(w1, {})
                list_bigrams[w1][w2] = list_bigrams[w1].get(w2, 0) + 1

            words_tri = []
            for s in sentences:
                tokens = nltk.word_tokenize(s.lower())
                tokens = [bos, bos] + tokens + [eos]
                for t in tokens:
                    if t not in {"(", ")", "[", "]", "{", "}", "``", "''", '"', "'", "--", "—"}:
                        t = t.lower()
                        words_tri.append(t)
            #print(pad_tri)
            for k in range(len(words_tri) - 2):
                w1 = words_tri[k]
                w2 = words_tri[k+1]
                w3 = words_tri[k+2]
                list_trigrams.setdefault((w1, w2), {})
                list_trigrams[(w1, w2)][w3] = list_trigrams[(w1, w2)].get(w3, 0) + 1
            #print(list_trigrams)
        #print("Done")

        print("Trigram")
        for i in range(1,6):
            print(f"{i}. {generate_trigram_sentence(list_trigrams)}")

        print("Bigram")
        for i in range(1,6):
            print(f"{i}. {generate_bigram_sentence(list_bigrams)}")

if __name__ == "__main__":
    main()
