import spacy
import re
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import sys

# -----------------------------
# Load models
# -----------------------------
nlp = spacy.load("en_core_web_lg")

# Coreference resolution via coreferee 
try:
    import coreferee
    if "coreferee" not in nlp.pipe_names:
        nlp.add_pipe("coreferee")
    COREF_AVAILABLE = True
    # print("[INFO] Coreference resolution enabled (coreferee).")
except Exception:
    COREF_AVAILABLE = False
    # print("[INFO] coreferee not available.")
    # print("       Install: pip install coreferee && python -m coreferee install en")

MODEL = "chatbot_relation_model_v2"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer  = BertTokenizer.from_pretrained(MODEL)
classifier = BertForSequenceClassification.from_pretrained(MODEL)
classifier.to(device)
classifier.eval()

ID2LABEL = {
    0: "parent",
    1: "child",
    2: "spouse",
    3: "sibling",
}

# -----------------------------
# Helper sets
# -----------------------------
WORD_TO_REL = {
    "parent": [
        "parent", "parents", "father", "dad", "mother", "mom", "mum",
        "father-in-law", "mother-in-law", "father in law", "mother in law",
        "stepfather", "stepmother",
    ],
    "child": [
        "child", "children", "son", "daughter",
        "stepson", "stepdaughter",
    ],
    "sibling": [
        "brother", "sister", "sibling", "siblings",
        "half-brother", "half-sister", "half brother", "half sister",
        "stepbrother", "stepsister",
    ],
    "spouse": [
        "husband", "wife", "spouse", "widow", "widower",
    ],
}

_WORD_LOOKUP = {}
for _rel, _words in WORD_TO_REL.items():
    for _w in _words:
        _WORD_LOOKUP[_w.lower()] = _rel
        _WORD_LOOKUP[_w.lower().replace("-", " ")] = _rel

_INVERSE = {
    "parent":  "child",
    "child":   "parent",
    "spouse":  "spouse",
    "sibling": "sibling",
}

_SUBJECT_PRONOUNS    = {"he", "she", "they"}
_POSSESSIVE_PRONOUNS = {"his", "her", "their"}

_RELN_WORDS = {
    "father", "mother", "parent", "parents",
    "child", "children", "son", "daughter",
    "brother", "sister", "siblings", "sibling",
    "husband", "wife", "spouse",
    "father-in-law", "mother-in-law",
    "half-brother", "half-sister",
    "stepfather", "stepmother", "stepson", "stepdaughter",
    "widow", "widower",
    "born to", "cousin",
}

UNSUPPORTED_TERMS = {
    "grandfather", "grandmother", "grandparent", "grandparents",
    "grandson", "granddaughter", "grandchild", "grandchildren",
    "great-grandfather", "great-grandmother", "great grandfather", "great grandmother",
    "great-great-grandfather", "great-great-grandmother",
    "uncle", "aunt", "cousin", "nephew", "niece"
}

# Demonyms / places / annotations SpaCy mislabels as PERSON
_NOT_PERSON = {
    "kenyan", "american", "irish", "english", "welsh", "german", "swiss",
    "african", "indonesian", "hawaiian", "japanese", "chinese", "indian",
    "french", "italian", "russian", "mexican", "canadian", "australian",
    "luo", "kogelo",
}

_BERT_LABEL_INVERSE = {
    # BERT label meaning:  main_subject → label → obj
    # "father" means obj IS the father of main_subject
    #   → from obj's side: obj → parent → main_subject
    # "mother" means obj IS the mother of main_subject
    #   → from obj's side: obj → parent → main_subject
    # "child"  means obj IS the child  of main_subject
    #   → from obj's side: obj → child  → main_subject  (main_subject is parent)
    "parent":  "child",
    "child":  "parent",
    "spouse":  "spouse",
    "sibling": "sibling",
}

NON_FAMILY_PATTERNS = [
    r"\bnamed after\b",
    r"\bworks? (?:at|for)\b",
    r"\bcolleague\b",
    r"\bfriend\b",
    r"\bteacher\b",
    r"\bmentor\b",
    r"\bcoach\b",
]

QUIT_STATEMENTS = {'q', 'quit'}

relation_table = {}

# =============================================================================
# Coreference resolution
# =============================================================================
def resolve_coreferences(text, main_subject):
    """
    Replace pronoun mentions of main_subject with the full name throughout
    the text using coreferee.  Gracefully returns original text on failure.
    """
    if not COREF_AVAILABLE or not main_subject:
        return text
    try:
        doc = nlp(text)
        replacements = {}
        for chain in doc._.coref_chains:
            chain_texts = [
                (m, " ".join(doc[i].text for i in m)) for m in chain
            ]
            first = main_subject.split()[0].lower()
            if not any(
                re.search(r"\b" + re.escape(first) + r"\b", t.lower())
                for _, t in chain_texts
            ):
                continue
            for mention, span_text in chain_texts:
                sl = span_text.lower()
                if sl in _SUBJECT_PRONOUNS | _POSSESSIVE_PRONOUNS:
                    repl = f"{main_subject}'s" \
                           if sl in _POSSESSIVE_PRONOUNS else main_subject
                    for idx in mention:
                        replacements[idx] = repl
        if not replacements:
            return text
        out, seen = [], set()
        for token in doc:
            if token.i in replacements and token.i not in seen:
                out.append(replacements[token.i])
                if token.whitespace_:
                    out.append(token.whitespace_)
                seen.add(token.i)
            else:
                out.append(token.text_with_ws)
        return "".join(out)
    except Exception as e:
        print(f"  [coref] Warning: {e}")
        return text


# =============================================================================
# Partial-name resolution
# =============================================================================
def resolve_partial_names(text):
    """
    Replace single-token person mentions (e.g. "Obama", "Swift") with their
    full name found earlier in the text.  Runs before sentence processing.
    """
    doc = nlp(text)
    person_entities = [
        {"text": ent.text, "start": ent.start_char, "end": ent.end_char}
        for ent in doc.ents
        if ent.label_ == "PERSON"
        and not is_spurious_person(normalize_entity_text(ent.text))
    ]

    # Build last-name → full-name and first-name → full-name maps
    last_to_full, first_to_full = {}, {}
    for ent in sorted(person_entities, key=lambda x: len(x["text"]), reverse=True):
        toks = ent["text"].split()
        if len(toks) >= 2:
            last  = toks[-1].lower()
            first = toks[0].lower()
            if last  not in last_to_full:  last_to_full[last]   = ent["text"]
            if first not in first_to_full: first_to_full[first] = ent["text"]

    # Collect replacements for single-word mentions
    replacements = []
    for ent in person_entities:
        toks = ent["text"].split()
        if len(toks) == 1:
            key  = toks[0].lower()
            full = last_to_full.get(key) or first_to_full.get(key)
            if full and full != ent["text"]:
                replacements.append(
                    {"start": ent["start"], "end": ent["end"], "new": full}
                )

    # Apply in reverse order to preserve character positions
    for rep in sorted(replacements, key=lambda x: x["start"], reverse=True):
        text = text[: rep["start"]] + rep["new"] + text[rep["end"]:]

    return text


# =============================================================================
# Utilities
# =============================================================================
def clean_sentence(text):
    return re.sub(r"\s+", " ", text.strip())

def normalize_name(name):
    return re.sub(r"\s+", " ", str(name)).strip()

def normalize_entity_text(text):
    """Strip possessive suffix SpaCy sometimes includes in an entity span."""
    return re.sub(r"'s$", "", text).strip()

def is_unsupported(sentence):
    s = sentence.lower()
    return any(re.search(r"\b" + re.escape(term) + r"\b", s) for term in UNSUPPORTED_TERMS)

def is_spurious_person(name):
    """True if this name is a demonym/place/annotation mislabelled as PERSON."""
    n = name.lower().strip()
    if n in _NOT_PERSON or n.startswith("née"):
        return True
    # Also reject if ANY token is a known demonym (catches "Luo Kenyan")
    if any(t in _NOT_PERSON for t in n.split()):
        return True
    return False

def name_tokens(name):
    return [t for t in re.findall(r"\w+", normalize_name(name).lower()) if t]

def build_aliases(full_name):
    toks = name_tokens(full_name)
    aliases = set()
    if not toks:
        return aliases

    aliases.add(" ".join(toks))
    aliases.add(toks[0])
    if len(toks) >= 2:
        aliases.add(f"{toks[0]} {toks[-1]}")

    suffixes = {"jr", "sr", "ii", "iii", "iv"}
    toks_ns = [t for t in toks if t not in suffixes]
    if toks_ns:
        aliases.add(" ".join(toks_ns))
        aliases.add(toks_ns[0])
        if len(toks_ns) >= 2:
            aliases.add(f"{toks_ns[0]} {toks_ns[-1]}")

    # Allow matching the full name with trailing punctuation stripped
    aliases.add(full_name.rstrip(".").strip())

    return sorted({a.strip() for a in aliases if a.strip()}, key=len, reverse=True)

def find_best_mention_span(text, full_name):
    text_lower = text.lower()
    for alias in build_aliases(full_name):
        m = re.search(r"\b" + re.escape(alias) + r"\b", text_lower)
        if m:
            return (m.start(), m.end())
    return None

def strip_shared_surname(relative, main_subject):
    """
    If the relative name ends with the same surname as main_subject
    (e.g. "Mary Ball Washington" and main_subject "George Washington"),
    strip the shared surname so BERT sees a clean name: "Mary Ball".
    This prevents the trailing shared name from confusing the classifier.
    """
    if not main_subject or not relative:
        return relative
    main_last = main_subject.split()[-1].lower()
    rel_toks   = relative.split()
    if len(rel_toks) > 1 and rel_toks[-1].lower() == main_last:
        return " ".join(rel_toks[:-1])
    return relative

def mark_entities_text(text, person, relative):
    """
    Insert [PERSON]..[/PERSON] and [RELATIVE]..[/RELATIVE] tags.
    Strips shared surname from relative name before matching to give
    BERT a cleaner input (e.g. "Mary Ball" instead of "Mary Ball Washington").
    Returns None if either name cannot be found or spans overlap.
    """
    # Strip shared surname for cleaner BERT input
    relative_clean = strip_shared_surname(relative, person)

    p_span = find_best_mention_span(text, person)
    r_span = find_best_mention_span(text, relative_clean)

    if p_span is None or r_span is None or p_span == r_span:
        return None

    spans = sorted(
        [("PERSON", p_span[0], p_span[1]),
         ("RELATIVE", r_span[0], r_span[1])],
        key=lambda x: x[1]
    )
    if spans[0][2] > spans[1][1]:   # overlapping
        return None

    out, last = [], 0
    for label, start, end in spans:
        out.append(text[last:start])
        out.append(f"[{label}] {text[start:end]} [/{label}]")
        last = end
    out.append(text[last:])
    return "".join(out)

def get_entity_text(ent):
    return normalize_entity_text(ent.text)

def deduplicate_persons(person_names):
    """
    1. Remove spurious / demonym names.
    2. Remove short names that are word-boundary substrings of a longer kept name.
    """
    person_names = [n for n in person_names if not is_spurious_person(n)]
    names = sorted(set(person_names), key=len, reverse=True)
    result = []
    for name in names:
        if not any(
            name != kept and re.search(r"\b" + re.escape(name) + r"\b", kept)
            for kept in result
        ):
            result.append(name)
    return result

def extract_person_entities_with_kin(doc, main_subject=None):
    """Return filtered, deduplicated PERSON entities from a SpaCy doc."""
    persons = [ent for ent in doc.ents if ent.label_ == "PERSON"]
    filtered = []
    for ent in persons:
        if is_spurious_person(get_entity_text(ent)):
            continue
        if len(ent.text.split()) == 1:
            inside = any(
                ent != other
                and ent.start >= other.start
                and ent.end <= other.end
                and len(other.text.split()) > 1
                for other in persons
            )
            if inside:
                continue
        filtered.append(ent)
    return filtered

def get_main_subject(doc):
    first_sent = list(doc.sents)[0]
    persons = extract_person_entities_with_kin(nlp(first_sent.text))
    if not persons:
        return None
    return max(persons, key=lambda e: len(e.text.split())).text.strip()

def resolve_pronouns(sentence, main_subject):
    """
    1. Replace a leading subject/possessive pronoun with the main subject.
    2. When coreferee is unavailable, also replace ALL mid-sentence subject
       and possessive pronouns so sentences like "Among his siblings, he was
       close to Lawrence" become parseable with full names.
    """
    if not main_subject:
        return sentence
    words = sentence.strip().split()
    if not words:
        return sentence

    # Leading pronoun replacement (always)
    first = words[0].lower()
    if first in _SUBJECT_PRONOUNS:
        sentence = sentence.replace(words[0], main_subject, 1)
    elif first in _POSSESSIVE_PRONOUNS:
        sentence = sentence.replace(words[0], f"{main_subject}'s", 1)

    # Mid-sentence replacement when coreferee is unavailable
    if not COREF_AVAILABLE:
        # Replace standalone subject pronouns → main_subject
        for pronoun in _SUBJECT_PRONOUNS:
            sentence = re.sub(
                r"\b" + pronoun + r"\b",
                main_subject,
                sentence,
                flags=re.IGNORECASE
            )
        # Replace possessive pronouns → main_subject's
        for pronoun in _POSSESSIVE_PRONOUNS:
            sentence = re.sub(
                r"\b" + pronoun + r"\b",
                f"{main_subject}'s",
                sentence,
                flags=re.IGNORECASE
            )

    return sentence

def is_deflected_relation(sentence, main_subject):
    """
    True when the sentence describes a relationship OF the main subject's
    relative, not of the subject directly.
    E.g. "George Washington's father had children from his marriage to Jane Butler"
    """
    if not main_subject:
        return False
    rp = "|".join(re.escape(w) for w in _RELN_WORDS)
    return bool(re.search(
        re.escape(main_subject) + r"'s\s+(?:" + rp + r")\b",
        sentence, re.IGNORECASE
    ))

def subject_is_only_possessive(sentence, main_subject):
    """
    True if main_subject appears ONLY as a possessive in this sentence
    (no standalone mention).  Excludes false matches inside longer names
    like "Barack Obama Sr."
    """
    if not main_subject:
        return False
    standalone = re.search(
        r"\b" + re.escape(main_subject) +
        r"\b(?!'s)(?!\s+(?:Sr|Jr|II|III|IV)\.?)",
        sentence, re.IGNORECASE
    )
    possessive = re.search(
        re.escape(main_subject) + r"'s", sentence, re.IGNORECASE
    )
    return possessive is not None and standalone is None

def is_non_family_sentence(sentence):
    return any(re.search(p, sentence, re.IGNORECASE) for p in NON_FAMILY_PATTERNS)

def is_alias_of(name, main_subject):
    if not main_subject or not name:
        return False
    return name.lower() in {a.lower() for a in build_aliases(main_subject)}

def has_reln_word(sentence):
    return any(h in sentence.lower() for h in _RELN_WORDS)

def token_rel(token):
    word = token.text.lower()
    return _WORD_LOOKUP.get(word) or _WORD_LOOKUP.get(word.replace("-", " "))

def get_person_from_token(token, doc):
    for ent in doc.ents:
        if ent.label_ == "PERSON" and ent.start <= token.i < ent.end:
            cleaned = normalize_entity_text(ent.text.strip())
            return None if is_spurious_person(cleaned) else cleaned
    return None

def get_person_or_propn(token, doc):
    p = get_person_from_token(token, doc)
    if p:
        return p
    if token.pos_ == "PROPN" and not is_spurious_person(token.text):
        return normalize_entity_text(token.text.strip())
    return None

def extract_coordinated_persons(token, doc):
    persons = []
    p = get_person_or_propn(token, doc)
    if p:
        persons.append(p)
    for child in token.children:
        if child.dep_ == "conj":
            cp = get_person_or_propn(child, doc)
            if cp:
                persons.append(cp)
    return persons

def same_clause(token_i, ent_start, doc):
    """
    Return True if the entity starting at ent_start is in the same
    dependency clause as the token at token_i.
    Heuristic: no verb or clause-boundary token between them.
    """
    for t in doc[token_i + 1: ent_start]:
        if t.dep_ in {"relcl", "advcl", "ccomp", "xcomp"} and t.pos_ == "VERB":
            return False
    return True


# =============================================================================
# Rule-based relationship extraction
# =============================================================================
def extract_relationships_from_sentence(sentence, main_subject):
    sentence = clean_sentence(sentence)
    sentence = resolve_pronouns(sentence, main_subject)

    doc = nlp(sentence)
    persons      = extract_person_entities_with_kin(doc, main_subject)
    person_texts = deduplicate_persons([get_entity_text(e) for e in persons])

    relationships = set()

    for token in doc:
        rel = token_rel(token)
        if rel is None:
            continue

        word = token.text.lower()

        # ------------------------------------------------------------------
        # CASE 1: "children of X and Y"
        # ------------------------------------------------------------------
        if word in {"child", "children", "son", "daughter"}:
            for ch in token.children:
                if ch.dep_ == "prep" and ch.text.lower() == "of":
                    for pobj in ch.children:
                        if pobj.ent_type_ == "PERSON" or pobj.pos_ == "PROPN":
                            parents = deduplicate_persons(
                                extract_coordinated_persons(pobj, doc)
                            )
                            for parent in parents:
                                if main_subject and parent != main_subject:
                                    relationships.add((main_subject, "child", parent))
                                    relationships.add((parent, "parent", main_subject))

        # ------------------------------------------------------------------
        # CASE 2: Possessive — "X's father/mother/… Y"
        #

        # ------------------------------------------------------------------
        for ch in token.children:
            if ch.dep_ == "poss":
                subject = get_person_from_token(ch, doc)
                if not subject and is_alias_of(ch.text, main_subject):
                    subject = main_subject
                if not subject:
                    continue
                for ent in persons:
                    obj = get_entity_text(ent)
                    if ent.start > token.i and obj not in (subject, ""):
                        if obj in person_texts and same_clause(token.i, ent.start, doc):
                            relationships.add((subject, rel, obj))
                            relationships.add((obj, _INVERSE[rel], subject))
                        break

        # ------------------------------------------------------------------
        # CASE 3: Copula — "X is/was the father/mother/… of Y"
        # ------------------------------------------------------------------
        if token.dep_ == "attr" and token.head.lemma_ == "be":
            for ent in persons:
                obj = get_entity_text(ent)
                if ent.start > token.i and obj not in (main_subject, ""):
                    if obj in person_texts:
                        relationships.add((main_subject, rel, obj))
                        relationships.add((obj, _INVERSE[rel], main_subject))
                    break

        # ------------------------------------------------------------------
        # CASE 4: Appositive — "Obama's mother, Ann Dunham"
        #                    or "her mother, Andrea Swift"
        #                    or "Swift's brother, Austin"
        #

        # ------------------------------------------------------------------
        if token.dep_ == "appos" and token.ent_type_ == "PERSON":
            # Get the full entity span this token belongs to
            obj_ent = next(
                (e for e in doc.ents
                 if e.label_ == "PERSON" and e.start <= token.i < e.end),
                None
            )
            obj = normalize_entity_text(
                obj_ent.text if obj_ent else token.text
            ).strip()
            if is_spurious_person(obj):
                continue

            head = token.head
            owner = None
            for ch in head.children:
                if ch.dep_ == "poss":
                    owner = get_person_from_token(ch, doc)
                    if owner:
                        owner = normalize_entity_text(owner)
                    elif ch.text.lower() in _POSSESSIVE_PRONOUNS:
                        owner = main_subject
                    elif is_alias_of(ch.text, main_subject):
                        owner = main_subject
                    break

            head_rel = token_rel(head)
            if head_rel and owner and obj != owner:
                relationships.add((owner, _INVERSE[head_rel], obj))
                relationships.add((obj, head_rel, owner))

        # ------------------------------------------------------------------
        # CASE 5: Sibling / half-sibling
        
        # ------------------------------------------------------------------
        if rel == "sibling":
            siblings_found = []
            for ent in persons:
                if ent.start > token.i and (ent.start - token.i) <= 10:
                    sib = get_entity_text(ent)
                    if sib in person_texts:
                        siblings_found.append(sib)
                    for conj in doc[ent.root.i].children:
                        if conj.dep_ == "conj":
                            cp = get_person_from_token(conj, doc)
                            if cp and cp in person_texts:
                                siblings_found.append(cp)
                    break
            for sib in deduplicate_persons(siblings_found):
                if main_subject and sib != main_subject:
                    relationships.add((main_subject, "sibling", sib))
                    relationships.add((sib, "sibling", main_subject))

    # Filter tuples referencing non-deduplicated (substring-covered) names.
    # The main subject is always exempt — it should never be filtered even
    # if another person (e.g. "Barack Obama Sr.") shares its tokens.
    all_known = set(person_texts) | ({main_subject} if main_subject else set())

    def is_covered(name):
        # Never filter the main subject itself
        if main_subject and name == main_subject:
            return False
        name_toks = set(name.lower().split())
        for kept in all_known:
            if kept == name:
                continue
            kept_toks = set(kept.lower().split())
            # Covered only if all tokens of name appear in kept AND kept is longer
            if name_toks.issubset(kept_toks) and len(kept_toks) > len(name_toks):
                return True
        return False

    return {
        (f, r, t) for f, r, t in relationships
        if not is_covered(f) and not is_covered(t)
    }


# =============================================================================
# BERT prediction
# =============================================================================
def predict_relation(input_text, min_conf=0.30):
    if input_text is None:
        return None, 0.0
    if "[PERSON]" not in input_text or "[RELATIVE]" not in input_text:
        return None, 0.0

    encoding = tokenizer(
        input_text,
        max_length=128,
        truncation=True,
        padding=True,
        return_tensors="pt",
    )
    encoding = {k: v.to(device) for k, v in encoding.items()}

    with torch.no_grad():
        outputs = classifier(**encoding)
        probs = torch.softmax(outputs.logits, dim=1)
        conf, pred_id = torch.max(probs, dim=1)

    pred_label = ID2LABEL[pred_id.item()]
    conf = conf.item()
    return (pred_label, conf) if conf >= min_conf else (None, conf)


# =============================================================================
# Parse text
# =============================================================================
def parse_text(text):
    # Step 1: detect main subject from raw text
    doc_raw      = nlp(text)
    main_subject = get_main_subject(doc_raw)
    # print(f"\nMain subject detected: {main_subject}")

    # Step 2: partial-name resolution ("Obama" → "Barack Obama")
    text = resolve_partial_names(text)

    # Step 3: coreference resolution (pronouns → full name)
    text = resolve_coreferences(text, main_subject)

    doc_full = nlp(text)

    # print("\n--- First few sentences (after pre-processing) ---")
    # for i, sent in enumerate(list(doc_full.sents)[:3]):
    #     print(f"Sentence {i}: {sent.text.strip()}")
    # print("--------------------------------------------------\n")

    results = set()

    for sent in doc_full.sents:
        sentence = clean_sentence(sent.text)
        sentence = resolve_pronouns(sentence, main_subject)

        doc_sent     = nlp(sentence)
        persons      = extract_person_entities_with_kin(doc_sent, main_subject)
        person_texts = deduplicate_persons([get_entity_text(e) for e in persons])

        # print(f"\nSentence: {sentence}")
        # print(f"  Detected PERSON entities: {person_texts}")

        if not person_texts:
            # print("  → No persons detected, skipping.")
            continue

        if is_non_family_sentence(sentence):
            # print("  → Non-family sentence, skipping.")
            continue

        if is_unsupported(sentence):
            # print("Unspported term for model, skipping")
            continue
        # ---- Rule-based ----
        rule_rels = extract_relationships_from_sentence(sentence, main_subject)

        all_known = set(person_texts) | ({main_subject} if main_subject else set())

        def _is_covered(name):
            if main_subject and name == main_subject:
                return False
            name_toks = set(name.lower().split())
            for kept in all_known:
                if kept == name:
                    continue
                kept_toks = set(kept.lower().split())
                if name_toks.issubset(kept_toks) and len(kept_toks) > len(name_toks):
                    return True
            return False

        rule_rels = {
            (f, r, t) for f, r, t in rule_rels
            if not _is_covered(f) and not _is_covered(t)
        }

        # if rule_rels:
        #     print(f"  → Rule-based: {rule_rels}")
        # else:
        #     print("  → No rule-based relationships found.")

        results.update(rule_rels)
        existing_pairs = {(f, t) for f, _, t in results}

        # Skip BERT for deflected / possessive-only sentences
        if is_deflected_relation(sentence, main_subject) or \
                subject_is_only_possessive(sentence, main_subject):
            # print("  → Deflected/possessive-only sentence, skipping BERT.")
            continue

        other_persons = [p for p in person_texts if p != main_subject]
        if not other_persons:
            # print("  → No other persons, skipping BERT.")
            continue

        if not has_reln_word(sentence):
            # print("  → No kin word, skipping BERT.")
            continue

        # ---- BERT ----
        for obj in other_persons:
            if (main_subject, obj) in existing_pairs:
                continue
            if main_subject not in sentence and not any(
                a in sentence for a in build_aliases(main_subject)
            ):
                continue

            marked = mark_entities_text(sentence, main_subject, obj)
            # print(f"  → Marked for BERT: {marked}")
            if marked is None:
                # print("  → Could not mark entities, skipping.")
                continue

            pred_rel, conf = predict_relation(marked)
            # print(f"  → BERT predicted: {pred_rel} ({conf:.2f})")
            if pred_rel is None:
                continue

            results.add((main_subject, pred_rel, obj))
            inv = _BERT_LABEL_INVERSE.get(pred_rel)
            if inv:
                results.add((obj, inv, main_subject))

    return results

def predict_only(text, min_conf=0.30):
    doc_raw = nlp(text)
    main_subject = get_main_subject(doc_raw)
    # print(f"\nMain subject detected: {main_subject}")

    if not main_subject:
        # print("  → No main subject detected.")
        return set()

    text = resolve_partial_names(text)
    text = resolve_coreferences(text, main_subject)
    doc_full = nlp(text)

    results = set()
    seen_pairs = set()

    for sent in doc_full.sents:
        sentence = clean_sentence(sent.text)
        sentence = resolve_pronouns(sentence, main_subject)

        doc_sent = nlp(sentence)
        persons = extract_person_entities_with_kin(doc_sent, main_subject)
        person_texts = deduplicate_persons([get_entity_text(e) for e in persons])

        # print(f"\nSentence: {sentence}")
        # print(f"  Detected PERSON entities: {person_texts}")

        if not person_texts:
            # print("  → No persons detected, skipping.")
            continue

        if is_non_family_sentence(sentence):
            # print("  → Non-family sentence, skipping.")
            continue

        if is_unsupported(sentence):
            # print("  → Unsupported kin term for 4-label model, skipping.")
            continue

        subject_present = (
            main_subject in sentence or
            any(re.search(r"\b" + re.escape(a) + r"\b", sentence, re.IGNORECASE)
                for a in build_aliases(main_subject))
        )
        if not subject_present:
            # print("  → Main subject not present in sentence, skipping.")
            continue

        other_persons = [p for p in person_texts if p != main_subject]
        if not other_persons:
            # print("  → No other persons, skipping BERT.")
            continue

        for obj in other_persons:
            if (main_subject, obj) in seen_pairs:
                continue
            seen_pairs.add((main_subject, obj))

            marked = mark_entities_text(sentence, main_subject, obj)
            # print(f"  → Marked for BERT: {marked}")
            if marked is None:
                print("  → Could not mark entities, skipping.")
                continue

            pred_rel, conf = predict_relation(marked, min_conf=min_conf)
            # print(f"  → BERT predicted: {pred_rel} ({conf:.2f})")
            if pred_rel is None:
                continue

            results.add((obj, pred_rel, main_subject))

            inv = _INVERSE.get(pred_rel)
            if inv:
                results.add((main_subject, inv, obj))

    return results


# =============================================================================
# Output
# =============================================================================
def print_ascii_tree(results):
    # Convert all triples to canonical (parent, child) form
    all_people = set()
    parent_child = set()
    spouse_pairs = set()
    sibling_pairs = set()

    for person, rel, target in results:
        all_people.add(person)
        all_people.add(target)
        if rel == "parent":
            parent_child.add((person, target))
        elif rel == "child":
            parent_child.add((target, person))
        elif rel == "spouse":
            spouse_pairs.add(tuple(sorted([person, target])))
        elif rel == "sibling":
            sibling_pairs.add(tuple(sorted([person, target])))

    # Remove contradictions: if (A, B) and (B, A) both in parent_child, drop both
    clean_parent_child = set()
    for parent, child in parent_child:
        if (child, parent) not in parent_child:
            clean_parent_child.add((parent, child))
    parent_child = clean_parent_child

    # Build graph
    graph = {p: {"parents": [], "children": [], "spouses": [], "siblings": []} for p in all_people}

    for parent, child in parent_child:
        if parent not in graph[child]["parents"]:
            graph[child]["parents"].append(parent)
        if child not in graph[parent]["children"]:
            graph[parent]["children"].append(child)

    for a, b in spouse_pairs:
        if b not in graph[a]["spouses"]:
            graph[a]["spouses"].append(b)
        if a not in graph[b]["spouses"]:
            graph[b]["spouses"].append(a)

    for a, b in sibling_pairs:
        if b not in graph[a]["siblings"]:
            graph[a]["siblings"].append(b)
        if a not in graph[b]["siblings"]:
            graph[b]["siblings"].append(a)

    # Siblings can't also be parents/children
    for person in all_people:
        siblings = set(graph[person]["siblings"])
        graph[person]["parents"]  = [p for p in graph[person]["parents"]  if p not in siblings]
        graph[person]["children"] = [p for p in graph[person]["children"] if p not in siblings]

    # Unify sibling groups transitively
    visited_sibs = set()
    sibling_groups = {}
    for person in sorted(all_people):
        if person in visited_sibs:
            continue
        group = set([person]) | set(graph[person]["siblings"])
        changed = True
        while changed:
            changed = False
            for m in list(group):
                new = set(graph.get(m, {}).get("siblings", []))
                if not new.issubset(group):
                    group |= new
                    changed = True
        if len(group) > 1:
            for m in group:
                sibling_groups[m] = sorted(group)
            visited_sibs.update(group)

    visited = set()

    def print_person(person):
        if person in visited:
            return
        visited.add(person)

        parents   = graph[person]["parents"]
        spouses   = graph[person]["spouses"]
        children  = graph[person]["children"]
        sib_group = sibling_groups.get(person, [])

        # Always print parents first
        if parents:
            parent_str = "  ─┬─  ".join(parents)
            bar_pos = len(parents[0]) + 3
            print(parent_str)
            print(" " * bar_pos + "│")
            for p in parents:
                visited.add(p)

        # Self row
        if sib_group:
            unvisited = [s for s in sib_group if s not in visited]
            if unvisited:
                print("  ─┼─  ".join(sib_group))
                for s in sib_group:
                    visited.add(s)
        elif spouses:
            spouse = spouses[0]
            print(f"{person}  ─┬─  {spouse}")
            visited.add(spouse)
            bar_pos = len(person) + 3
            if children:
                print(" " * bar_pos + "│")
                for i, child in enumerate(children):
                    connector = "└──" if i == len(children) - 1 else "├──"
                    print(" " * bar_pos + connector + " " + child)
                    visited.add(child)
        else:
            print(person)

        print()

    # Print people who have parents first so the tree anchors correctly
    for person in sorted(all_people):
        if person in visited:
            continue
        if graph[person]["parents"]:
            print_person(person)

    # Print anyone remaining
    for person in sorted(all_people):
        if person not in visited:
            print_person(person)

def print_results(results):
    if not results:
        print("No family relationships found.")
        return
    for frm, rel, to in sorted(results):
        print(f"{frm} → {rel} → {to}")

# =============================================================================
# CLI
# =============================================================================


def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            text = f.read()

        rb_results = parse_text(text)
        print("Rule Based Extraction\n")
        print_results(rb_results)

        results = predict_only(text)
        # print(results)
        print(" ")
        print("Classifier Tree Results\n")
        print_ascii_tree(results)

    elif len(sys.argv) == 1:
        while True:
            text = input("] ")
            if text.lower() in QUIT_STATEMENTS:
                exit()
            rb_results = parse_text(text)
            print("Rule Based Extraction\n")
            print_results(rb_results)

            results = predict_only(text)
            print_ascii_tree(results)

    else:
        raise ValueError("Too many arguments")

if __name__ == "__main__":
    main()




