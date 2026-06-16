
import re
import sys
import json
import time
import spacy
import urllib.request
import urllib.parse
from SPARQLWrapper import SPARQLWrapper, JSON

WIKI_DELAY = 0.5
BATCH_DELAY = 2.0
TOTAL_EXAMPLES = 5000
HONORIFICS = {
    "sir", "dame", "lord", "lady", "mr", "mrs", "ms", "dr", "prof",
    "professor", "rev", "reverend", "hon", "the", "st", "saint",
    "duke", "duchess", "earl", "count", "countess", "baron", "baroness",
    "prince", "princess", "king", "queen", "emperor", "empress",
}
RELATION_HINTS = {
    "father": ["father", "dad", "son of", "daughter of"],
    "mother": ["mother", "mom", "mum", "son of", "daughter of"],
    "child": ["son", "daughter", "child", "children"],
    "spouse": ["wife", "husband", "spouse", "married", "married to"],
    "sibling": ["brother", "sister", "sibling", "siblings"],
}

endpoint_url = "https://query.wikidata.org/sparql"
user_agent = "csc482-project Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
nlp = spacy.load("en_core_web_lg")

people_query = """
SELECT DISTINCT ?person ?personLabel ?article
WHERE {
  ?person wdt:P31 wd:Q5;
          wdt:P22|wdt:P25 [].
  ?article schema:about ?person ;
           schema:isPartOf <https://en.wikipedia.org/> .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
}
LIMIT 500
"""

relations_query = """
SELECT ?relative ?relativeLabel ?relation
WHERE {{
  BIND(<{person_id}> AS ?person)

  {{ ?person wdt:P22   ?relative . BIND("father"  AS ?relation) }}
  UNION
  {{ ?person wdt:P25   ?relative . BIND("mother"  AS ?relation) }}
  UNION
  {{ ?person wdt:P40   ?relative . BIND("child"   AS ?relation) }}
  UNION
  {{ ?person wdt:P26   ?relative . BIND("spouse"  AS ?relation) }}
  UNION
  {{ ?person wdt:P3373 ?relative . BIND("sibling" AS ?relation) }}

  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
}}
"""

# get wikidata relations
def sparql_query(q):
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(q)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()["results"]["bindings"]

# get text from wikipedia
def get_wikipage(url):
    try:
        title  = url.split("/wiki/")[-1]
        params = urllib.parse.urlencode({
            "action": "query",
            "prop": "revisions",
            "titles": urllib.parse.unquote(title),
            "rvprop": "content",
            "rvslots": "main",
            "format": "json",
        })
        api_url = f"https://en.wikipedia.org/w/api.php?{params}" 
        req = urllib.request.Request(api_url, headers={"User-Agent": user_agent})
        with urllib.request.urlopen(req, timeout=20) as r:
            data  = json.loads(r.read().decode())
            pages = data["query"]["pages"]
            page  = next(iter(pages.values()))
            wikitext = page["revisions"][0]["slots"]["main"]["*"]
            return clean_wikitext(wikitext)
    except Exception as e:
        print(f"failed to get article for {url}: {e}")
        return ""

# manually clean wikitext 
def clean_wikitext(text):
    """Strip wikitext markup to get readable plain text."""
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'\{\{[^}]+\}\}', '', text)
    text = re.sub(r'<ref[^>]*>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text) 
    text = re.sub(r"'{2,3}", '', text)
    text = re.sub(r'\[https?://\S+\s*([^\]]*)\]', r'\1', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def token_in_name(token, name_text):
    return token.lower() in re.findall(r"\w+", name_text.lower())

# get sentences where person is mentioned
#TODO: coreference resolution to improve matches, maybe only take sentences with both mentioned
def get_mentions(doc, person, relative):
    person_first = get_first_name(person)
    relative_first = get_first_name(relative)

    # if first names are the same, fall back to full name
    if person_first == relative_first:
        relative_first = relative

    matches = []
    for sent in doc.sents:
        people = {ent.text for ent in sent.ents if ent.label_ == "PERSON"}
        if not people:
            continue
        
        person_match = None
        relative_match = None
        
        for ent_text in people:
            ent_lower = ent_text.lower()

            if person_match is None and token_in_name(person_first, ent_text):
                person_match = ent_text

            if token_in_name(relative_first, ent_text):
                relative_match = ent_text

        if person_match and relative_match and person_match != relative_match:
            matches.append({
                "text": sent.text.strip(),
                "person_mention": person_match,
                "relative_mention": relative_match,
            })

    return matches

def replace_once(text, target, repl):
    pattern = re.escape(target)
    out, n = re.subn(pattern, repl, text, count=1)
    return out if n > 0 else text

def mark_entities_text(text, person_mention, relative_mention):
    pairs = sorted(
        [
            (person_mention, f"[PERSON] {person_mention} [/PERSON]"),
            (relative_mention, f"[RELATIVE] {relative_mention} [/RELATIVE]")
        ],
        key=lambda x: len(x[0]),
        reverse=True
    )

    for raw, tagged in pairs:
        text = replace_once(text, raw, tagged)

    if "[PERSON]" not in text or "[RELATIVE]" not in text:
        return None

    return text

def has_relation_hint(text, relation):
    s = text.lower()
    return any(hint in s for hint in RELATION_HINTS.get(relation, []))

def get_first_name(full_name):
    tokens = full_name.lower().split()
    for token in tokens:
        cleaned = token.strip(".,")
        if cleaned not in HONORIFICS:
            return cleaned
    return tokens[0]  # fallback

def main():
    dataset = []
    num_missed = 0
    counts = {"father": 0, "mother": 0, "child": 0, "spouse": 0, "sibling": 0}

    print("Fetching people pool...")
    people_rows = sparql_query(people_query)

    people = {}
    for row in people_rows:
        person_id = row["person"]["value"]
        person_name = row["personLabel"]["value"]
        article_url = row.get("article", {}).get("value", "")

        if person_id not in people:
            people[person_id] = {
                "person_name": person_name,
                "article_url": article_url,
            }

    people_items = list(people.items())
    print(f"Loaded {len(people_items)} people")

    stop = False

    for i, (person_id, info) in enumerate(people_items, start=1):
        if len(dataset) >= TOTAL_EXAMPLES:
            break

        person_name = info["person_name"]
        article_url = info["article_url"]

        print(f"[{i}/{len(people_items)}] Processing: {person_name}")

        try:
            relation_rows = sparql_query(relations_query.format(person_id=person_id))
        except Exception as e:
            print(f"\tFailed to get relations for {person_name}: {e}")
            continue

        relations = []
        for rel_row in relation_rows:
            relative_name = rel_row["relativeLabel"]["value"]
            relation = rel_row["relation"]["value"]

            if "/.well-known/genid/" in relative_name or relative_name.startswith("http"):
                continue

            relations.append((relative_name, relation))

        if not relations:
            continue

        text = get_wikipage(article_url)
        if not text:
            num_missed += 1
            continue

        doc = nlp(text)

        for relative, relation in relations:
            mentions = get_mentions(doc, person_name, relative)

            for mention in mentions:
                if not has_relation_hint(mention["text"], relation):
                    continue

                tagged_text = mark_entities_text(
                    mention["text"],
                    mention["person_mention"],
                    mention["relative_mention"]
                )
                if tagged_text is None:
                    continue

                dataset.append({
                    "text": mention["text"],
                    "input_text": tagged_text,
                    "person": person_name,
                    "relative": relative,
                    "person_mention": mention["person_mention"],
                    "relative_mention": mention["relative_mention"],
                    "relation": relation,
                })
                counts[relation] = counts.get(relation, 0) + 1

                if len(dataset) >= TOTAL_EXAMPLES:
                    stop = True
                    break

            if stop:
                break

        time.sleep(WIKI_DELAY)

        if i % 10 == 0 or stop:
            print(f"\nCheckpoint save at {i} people...")
            deduped = []
            seen = set()
            for row in dataset:
                key = (
                    row["text"].strip().lower(),
                    row["person"].strip().lower(),
                    row["relative"].strip().lower(),
                    row["relation"].strip().lower(),
                )
                if key not in seen:
                    seen.add(key)
                    deduped.append(row)

            dataset = deduped

            with open("wikidata_updated.json", "w", encoding="utf-8") as f:
                json.dump(dataset, f, indent=2, ensure_ascii=False)

            print(f"Running counts: {counts}  (total: {sum(counts.values())})")

        if stop:
            break

        time.sleep(BATCH_DELAY)

    # final dedupe
    deduped = []
    seen = set()
    for row in dataset:
        key = (
            row["text"].strip().lower(),
            row["person"].strip().lower(),
            row["relative"].strip().lower(),
            row["relation"].strip().lower(),
        )
        if key not in seen:
            seen.add(key)
            deduped.append(row)

    dataset = deduped

    with open("wikidata_updated.json", "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)

    print(f"\nDone. {len(dataset)} examples, {num_missed} missed")
    print(f"Final counts: {counts}")

if __name__ == "__main__":
    main()


# 500 people, Running counts: {'father': 351, 'mother': 366, 'child': 678, 'spouse': 311, 'sibling': 753}  (total: 2459)

