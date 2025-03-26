import os
import spacy
import json
import re
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

DATA_FOL = "data/processed_texts"
OUTPUT_FOL = "data/relations.json"

# 🔹 Garbage entities to remove
INVALID_ENTITIES = {"-", "of", "from", "to", "it", "this", "that", "these", "those", "there", "here", "we", "they",
                    "for", "a", "an", "the", "and", "or", "with", "on", "by", "at", "as", "from", "in", "out", "under",
                    "over", "above", "below", "up", "down", "into", "onto", "but"}

# 🔹 Meaningless verbs to ignore
INVALID_RELATIONS = {"use", "using", "apply", "applying", "choose", "chooses", "incorporate", "incorporating",
                     "perform", "performs", "achieve", "achieves", "present", "see", "need", "have", "get", "show",
                     "model", "obtain", "alleviate"}

# 🔹 Ensure multi-word entity grouping
matcher = Matcher(nlp.vocab)
matcher.add("MULTI_WORD_ENTITY", [[{"POS": "PROPN"}, {"POS": "PROPN"}]])  # e.g., "BERT Model"


def extract_relations(text):
    doc = nlp(text)
    relations = []
    entity_map = {}

    # 🔹 Step 1: Capture Named Entities & Multi-word Entities
    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        entity_map[span.root] = span.text  # Store full entity phrase

    for ent in doc.ents:
        entity_map[ent.root] = ent.text  # Ensure Named Entities are stored correctly

    # 🔹 Step 2: Extract Relations
    for token in doc:
        entity1 = entity_map.get(token, token.text)
        entity2 = entity_map.get(token.head, token.head.text)

        # 🔹 Step 3: Normalize Entities
        entity1 = entity1.strip()
        entity2 = entity2.strip()

        # 🔹 Ignore invalid entities
        if entity1.lower() in INVALID_ENTITIES or entity2.lower() in INVALID_ENTITIES:
            continue
        if len(entity1) <= 2 or len(entity2) <= 2:
            continue  # Ignore very short junk words
        if entity1 == entity2:
            continue  # Avoid self-referencing entities like "BERT → model → model"

        # 🔹 Step 4: Extract Subject-Verb-Object (SVO) Relations
        if token.dep_ in ("nsubj", "dobj", "pobj") and token.head.pos_ == "VERB":
            verb = token.head.lemma_

            if verb in INVALID_RELATIONS:
                continue  # Ignore generic verbs

            relations.append({"Entity1": entity1, "Relation": verb, "Entity2": entity2})

        # 🔹 Step 5: Handle Passive Voice (e.g., "BooksCorpus is used to train BERT")
        elif token.dep_ == "nsubjpass" and token.head.pos_ == "VERB":
            verb = token.head.lemma_ + "_by"
            relations.append({"Entity1": entity2, "Relation": verb, "Entity2": entity1})

        # 🔹 Step 6: Capture "X is a type of Y" (Appositional)
        elif token.dep_ == "appos":
            relations.append({"Entity1": entity1, "Relation": "also_called", "Entity2": entity2})

        # 🔹 Step 7: Capture "X is part of Y" (Prepositional)
        elif token.dep_ == "prep" and token.head.pos_ in ("NOUN", "PROPN"):
            relations.append({"Entity1": entity1, "Relation": "part_of", "Entity2": entity2})

    return relations


def process_all_texts():
    all_relations = []
    
    for filename in os.listdir(DATA_FOL):
        if filename.endswith(".txt"):
            text_path = os.path.join(DATA_FOL, filename)
            with open(text_path, "r", encoding="utf-8") as f:
                text = f.read()

            relations = extract_relations(text)
            all_relations.extend(relations)
            print(f"Extracted {len(relations)} relations from {filename}")

    # 🔹 Step 8: Remove duplicate relations
    all_relations = [dict(t) for t in {tuple(d.items()) for d in all_relations}]

    with open(OUTPUT_FOL, "w") as f:
        json.dump(all_relations, f, indent=4)

    print(f"Saved {len(all_relations)} relations to {OUTPUT_FOL}")


if __name__ == "__main__":
    process_all_texts()
