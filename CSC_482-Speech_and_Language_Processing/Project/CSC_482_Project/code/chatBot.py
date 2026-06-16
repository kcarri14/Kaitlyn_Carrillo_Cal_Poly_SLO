import spacy
import re
import argparse
import pickle
import sys
# -----------------------------
# Load models
# -----------------------------
nlp = spacy.load("en_core_web_sm")

with open("relation_classifier.pkl", "rb") as f:
    classifier = pickle.load(f)

# -----------------------------
# Helper sets
# -----------------------------
WORD_TO_REL = {
    "parent": ["parent", "parents", "father", "dad", "mother", "mom", "mum"],
    "child": ["child", "children", "son", "daughter"],
    "sibling": ["brother", "sister"],
    "spouse": ["husband", "wife", "spouse"],
}
_WORD_LOOKUP = {w.lower(): k for k, words in WORD_TO_REL.items() for w in words}
_INVERSE = {
    "parent": "child",
    "child": "parent",
    "spouse": "spouse",
    "sibling": "sibling",
}
_SUBJECT_PRONOUNS = {"he", "she", "they"}
_POSSESSIVE_PRONOUNS = {"his", "her", "their"}

# key: relative, value: relation
relation_table = {}

# -----------------------------
# Utilities
# -----------------------------
def clean_sentence(text):
    return re.sub(r"\(.*?\)", "", text)

def extract_person_entities(doc):
    persons = [ent for ent in doc.ents if ent.label_ == "PERSON"]
    filtered = []
    for ent in persons:
        if len(ent.text.split()) == 1:
            inside_larger = any(
                ent != other
                and ent.start >= other.start
                and ent.end <= other.end
                and len(other.text.split()) > 1
                for other in persons
            )
            if inside_larger:
                continue
        filtered.append(ent)
    return filtered

def get_main_subject(doc):
    first_sent = list(doc.sents)[0]
    persons = extract_person_entities(first_sent)
    if not persons:
        return None
    return max(persons, key=lambda e: len(e.text.split())).text.strip()

def resolve_pronouns(sentence, main_subject):
    words = sentence.strip().split()
    if not words or not main_subject:
        return sentence
    if words[0].lower() in _SUBJECT_PRONOUNS:
        return sentence.replace(words[0], main_subject, 1)
    if words[0].lower() in _POSSESSIVE_PRONOUNS:
        return f"{main_subject} {sentence}"
    return sentence

def get_person_from_token(token, doc):
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.start <= token.i < ent.end:
            return ent.text.strip()
    return None

def extract_coordinated_persons(token, doc):
    persons = []
    person = get_person_from_token(token, doc)
    if person:
        persons.append(person)
    for child in token.children:
        if child.dep_ == "conj":
            conj_person = get_person_from_token(child, doc)
            if conj_person:
                persons.append(conj_person)
    return persons

# -----------------------------
# Rule-based relationship extraction
# -----------------------------
def extract_relationships_from_sentence(sentence, main_subject):
    sentence = clean_sentence(sentence)
    sentence = resolve_pronouns(sentence, main_subject)

    doc = nlp(sentence)
    persons = extract_person_entities(doc)
    relationships = set()

    for token in doc:
        word = token.text.lower()
        if word not in _WORD_LOOKUP:
            continue
        rel = _WORD_LOOKUP[word]

        # CASE 1: "children of X and Y"
        if word in {"child", "children", "son", "daughter"}:
            for child in token.children:
                if child.dep_ == "prep" and child.text.lower() == "of":
                    for pobj in child.children:
                        if pobj.ent_type_ == "PERSON":
                            parents = extract_coordinated_persons(pobj, doc)
                            for parent in parents:
                                if main_subject and parent != main_subject:
                                    relationships.add((main_subject, "child", parent))
                                    relationships.add((parent, "parent", main_subject))

        # CASE 2: Possessive
        for child in token.children:
            if child.dep_ == "poss":
                subject = get_person_from_token(child, doc)
                if not subject:
                    continue
                for ent in persons:
                    if ent.start > token.i:
                        obj = ent.text.strip()
                        if subject != obj:
                            relationships.add((subject, rel, obj))
                            relationships.add((obj, _INVERSE[rel], subject))
                        break

        # CASE 3: Copula
        if token.dep_ == "attr" and token.head.lemma_ == "be":
            for ent in persons:
                if ent.start > token.i:
                    obj = ent.text.strip()
                    if main_subject and obj != main_subject:
                        relationships.add((main_subject, rel, obj))
                        relationships.add((obj, _INVERSE[rel], main_subject))
                    break

        # CASE 4: Appositive
        if token.dep_ == "appos" and token.ent_type_ == "PERSON":
            obj = token.text.strip()
            head = token.head
            rel_word = head.text.lower()
            if rel_word in _WORD_LOOKUP and main_subject:
                rel = _WORD_LOOKUP[rel_word]
                relationships.add((main_subject, rel, obj))
                relationships.add((obj, _INVERSE[rel], main_subject))

        # CASE 5: Sibling mentions
        if word in {"brother", "sister"}:
            for ent in persons:
                if ent.start > token.i:
                    sibling = ent.text.strip()
                    if main_subject and sibling != main_subject:
                        relationships.add((main_subject, "sibling", sibling))
                        relationships.add((sibling, "sibling", main_subject))
                    break

    return relationships

# -----------------------------
# ML classifier prediction
# -----------------------------
def predict_relation(sentence):
    return classifier.predict([sentence])[0]

# -----------------------------
#  Parse text 
# -----------------------------
def parse_text(text):
    doc = nlp(text)
    main_subject = get_main_subject(doc)
    results = set()

    for sent in doc.sents:
        sentence = clean_sentence(sent.text)
        sentence = resolve_pronouns(sentence, main_subject)
        persons = extract_person_entities(nlp(sentence))

        if not persons:
            continue

        #  Apply rule-based extraction
        rule_rels = extract_relationships_from_sentence(sentence, main_subject)
        results.update(rule_rels)

        print("res", results)

        # Apply classifier for any PERSON pairs not caught by rules
        for ent in persons:
            obj = ent.text.strip()
            if main_subject and obj != main_subject:
                print(main_subject, obj)
                pred_rel = predict_relation(sentence)
                print(f"getting relationship from classifier: {pred_rel}, {obj}")
                results.add((main_subject, pred_rel, obj))

    return results

# -----------------------------
# Print results
# -----------------------------
def print_results(results):
    if not results:
        print("No family relationships found.")
        return
    for frm, rel, to in sorted(results):
        print(f"{frm} → {rel} → {to}")

# -----------------------------
# CLI
# -----------------------------
      
def main():
    if len(sys.argv) == 2:
        # file provided
        file_path = sys.argv[1]
        with open(file_path, "r") as f:
            text = f.read()

        results = parse_text(text)
        print_results(results)

    elif len(sys.argv) == 1:
        # chatBot
        while True:
            text = str(input("] "))
            results = parse_text(text)
            print_results(results)
            
    else:
        # too many args
        raise ValueError("Too many arguments")

if __name__ == "__main__":
    main()
