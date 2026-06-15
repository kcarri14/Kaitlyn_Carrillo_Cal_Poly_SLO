import nltk
# nltk.download("cmudict")
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger_eng')
from nltk.tokenize import sent_tokenize
from nltk.corpus import cmudict
import syllables
import sys
from nltk import pos_tag, word_tokenize


def flesch_kincade(words, sentences, syllables):
    grade = (0.39 * (words /sentences)) + (11.8 * (syllables / words)) -15.59
    return grade

def dale_chall(difficult, words, sentences):
    if((difficult / words) <= 0.05):
        score = (0.1579 * ((difficult / words) * 100)) + (0.0496 *(words / sentences))
    else:
        score = (0.1579 * ((difficult / words) * 100)) + (0.0496 *(words / sentences)) + 3.6365
    return score

def gunning_fog(complex_words, words, sentences):
    return (0.4 * ((words/sentences) + (100 * (complex_words / words))))

def main():
    if (len(sys.argv) < 2):
        print("No file provided!")
        return
    input_path = sys.argv[1]
    
    with open(input_path, "r", encoding='utf-8') as f:
        files = f.read()

    with open("dalechall.txt", "r", encoding='utf-8') as f:
        dalechall = set(line.strip().lower() for line in f if line.strip())

    word_tokens = nltk.word_tokenize(files)
    total_word = len(word_tokens)

    sentence_tokens = nltk.sent_tokenize(files)
    print(sentence_tokens)
    sentence_count = len(sentence_tokens)

    total_syallable = 0
    d = cmudict.dict()
    for word in word_tokens: 
        w = word.lower()
        if not w.isalpha():
            continue
        if w not in d:
            total_syallable = total_syallable + syllables.estimate(w)
        else:
            pronunciation = d[w][0]
            total_syallable = total_syallable + len([phone for phone in pronunciation if phone[-1].isdigit()])

    total_difficult = 0
    for words in word_tokens:
        if words.isalpha() and words.lower() not in dalechall:
            total_difficult += 1
    # print(total_difficult)
    # print(total_word)
    # print(total_syallable)
    # print(sentence_count)

    total_complex = 0
    tagged = pos_tag(word_tokens)
    print(tagged)

    for token, tag in tagged:
        if not token.isalpha():
            continue
        if tag in ("NNP", "NNPS"):  
            continue
        if any(ch in token for ch in "-/_"):
            continue
        w = token.lower()
        if w.endswith("'s"):
            w = w[:-2]
        if len(w) > 5 and w.endswith("ing"):
            w = w[:-3]
        if len(w) > 4 and w.endswith("ed"):
            w = w[:-2]
        if len(w) > 4 and w.endswith("es"):
            w = w[:-2]
            
            if w not in d:
                total_syallables = syllables.estimate(word)
                if (total_syallables >= 3):
                    total_complex += total_syallables
            else:
                pronunciation = d[w][0]
                syallable = len([phone for phone in pronunciation if phone[-1].isdigit()])
                if (syallable >= 3):
                    total_complex = total_complex + syallable

    score_flesch = flesch_kincade(total_word, sentence_count, total_syallable)
    flesch_grade = None
    if (score_flesch == 100.00 and score_flesch >= 90.00):
        flesch_grade = "5th grade"
    elif(score_flesch < 90.00 and score_flesch >= 80.00):
        flesch_grade = "6th Grade"
    elif(score_flesch < 80.00 and score_flesch >= 70.00):
        flesch_grade = "7th Grade"
    elif(score_flesch < 70.00 and score_flesch >= 60.00):
        flesch_grade = "8th and 9th Grade"
    elif(score_flesch < 60.00 and score_flesch >= 50.00):
        flesch_grade = "10th to 12th Grade"
    elif(score_flesch < 50.00 and score_flesch >= 30.00):
        flesch_grade = "College"
    elif(score_flesch < 30.00 and score_flesch >= 10.00):
        flesch_grade = "College Graduate"
    elif(score_flesch < 10.00 and score_flesch >= 0.00):
        flesch_grade = "Professional"

    dale_grade = None
    score_dale = dale_chall(total_difficult, total_word, sentence_count)
    if (score_dale <= 4.9):
        dale_grade = "Grade 4 and below"
    elif(score_dale < 5.9 and score_dale >= 5.0):
        dale_grade = "Grades 5–6"
    elif(score_dale < 6.9 and score_dale >= 6.0):
        dale_grade = "Grades 7–8"
    elif(score_dale < 7.9 and score_dale >= 7.0):
        dale_grade = "Grades 9–10"
    elif(score_dale < 8.9 and score_dale <= 8.0):
        dale_grade = "Grades 11–12"
    elif(score_dale < 9.9 and score_dale <= 9.0):
        dale_grade = "Grades 13–15 (college)"
    elif(score_dale >= 10.00):
        dale_grade = "Grades 16 and above."

    print(f"Flesch-Kincade grade level: {flesch_grade}")
    print(f"Dale-Chall Readability Formula: {dale_grade} ")
    print(f"Gunning-Fog index: {gunning_fog(total_complex, total_word, sentence_count)} ")



if __name__ == "__main__":
    main()

    