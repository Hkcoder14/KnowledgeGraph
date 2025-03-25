import spacy
import os
import json

nlp = spacy.load("en_core_web_sm")

DATA_FOL = "/Volumes/Personal/Knowledge-Graph/data/processed_texts"
OUTPUT_FOL = "/Volumes/Personal/Knowledge-Graph/data/entities.json"


def extract_entities(text):
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({"text": ent.text, "label": ent.label_})
    return entities

def process_all_text_files():

    all_entities = []
    for filename in os.listdir(DATA_FOL):
        if filename.endswith(".txt"):
            text_path = os.path.join(DATA_FOL, filename)
            with open(text_path, "r", encoding="utf-8") as f:
                text = f.read()

            entities = extract_entities(text)
            all_entities.extend(entities)

    with open(OUTPUT_FOL, "w") as f:
        json.dump(all_entities, f, indent=4)

    print(f"Entites are saved into {OUTPUT_FOL}")


# Run the extraction
if __name__ == "__main__":
    process_all_text_files()