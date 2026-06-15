import nltk
from nltk.corpus import udhr
import sys
import math
languages = [ 'Afrikaans-Latin1', 'Danish_Dansk-Latin1', 'Dutch_Nederlands-Latin1', 
             'English-Latin1', 'French_Francais-Latin1', 'German_Deutsch-Latin1', 'Indonesian-Latin1', 
             'Italian-Latin1', 'Spanish-Latin1','Swedish_Svenska-Latin1']

languages_output = { 'Afrikaans-Latin1': "Afrikaans", 
                    'Danish_Dansk-Latin1': "Danish", 
                    'Dutch_Nederlands-Latin1': "Dutch", 
             'English-Latin1': "English", 
             'French_Francais-Latin1': "French", 
             'German_Deutsch-Latin1': "German", 
             'Indonesian-Latin1': "Indonesian", 
             'Italian-Latin1': "Italian", 
             'Spanish-Latin1': "Spanish",
             'Swedish_Svenska-Latin1': "Swedish"}

def main():
    input_path = sys.argv[1]
    with open(input_path, "r", encoding='utf-8') as f:
        files = f.read()

    counts_input = {}
    files = files.lower()
    trigram_input = []
    for i in range(len(files) - 2):
        trigram_input.append(files[i:i+3])

    for tri in trigram_input:
        counts_input[tri] = counts_input.get(tri, 0) + 1

    list_languages = {}
    list_vocab = {}
    for i in languages:
        counts = {}
        results = udhr.raw(i)
        results = results.lower()
        trigram = []
        for j in range(len(results) - 2):
            trigram.append(results[j:j+3])
        for tri in trigram:
            counts[tri] = counts.get(tri, 0) + 1

        list_languages[i] = counts
        list_vocab[i] = sum(counts.values())

    V = len(list_vocab)
    best_language = None
    best_score = 0

    for f in languages:
        denominator = list_vocab[f] + V
        score = 0.0

        language_counts = list_languages[f]
        for gram, count in counts_input.items():
            count_lang = language_counts.get(gram, 0)
            probability = (count_lang + 1) / denominator
            score += count * probability

        if best_language is None or score > best_score:
            best_score = score
            best_language = f
    
    print(languages_output[best_language])        

if __name__ == "__main__":
    main()

