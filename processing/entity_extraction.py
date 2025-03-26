import spacy
import os
import json

nlp = spacy.load("en_core_web_sm")

DATA_FOL = "/Volumes/Personal/Knowledge-Graph/data/processed_texts"
OUTPUT_FOL = "/Volumes/Personal/Knowledge-Graph/data/entities.json"


# 🔹 Manually Define AI/ML-Specific Terms (to catch missing entities)
AI_TERMS = {"BERT", "Transformer", "Fine-tuning", "Masked LM", "Language Model", "Pre-training", "Self-Attention", 
            "Multi-Head Attention", "WordPiece", "Tokenization", "Hidden States", "Next Sentence Prediction"}

def extract_entities(text):
    doc = nlp(text)
    entities = []

    for ent in doc.ents:
        entities.append({"text": ent.text, "label": ent.label_})

    # 🔹 Capture noun chunks (like "BERT Model", "Masked Language Model") if spaCy missed them
    for chunk in doc.noun_chunks:
        if chunk.text not in [e["text"] for e in entities]:  # Avoid duplicates
            entities.append({"text": chunk.text, "label": "CONCEPT"})  # Generic label for unknown terms

    # 🔹 Ensure AI-specific terms are always included
    for term in AI_TERMS:
        if term in text and term not in [e["text"] for e in entities]:
            entities.append({"text": term, "label": "AI_TERM"})

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