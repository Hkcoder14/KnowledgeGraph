import os
import spacy
import json

nlp = spacy.load("en_core_web_sm")

DATA_FOL = "data/processed_texts"
OUTPUT_FOL = "data/relations.json"

def extract_relations(text):
    doc = nlp(text)
    relations = []

    for token in doc:
        if token.dep_ in ("nsubj", "dobj", "pobj", "appos"):
            subject = token.head.text
            relation = token.dep_
            object_= token.text
            relations.append({"Entity 1": subject, "Relation": relation, "Entity 2": object_})

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
            print(f"extracted realations from {filename}")
        
    with open(OUTPUT_FOL, "w") as f:
        json.dump(all_relations, f, indent=4)

    print(f"Saved Relations to {OUTPUT_FOL}")

#Run the extraction
if __name__ == "__main__":
    process_all_texts()
