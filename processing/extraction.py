import os
import fitz

DATA_FOL = "/Volumes/Personal/Knowledge-Graph/data/papers"
OUTPUT_FOL = "/Volumes/Personal/Knowledge-Graph/data/processed_texts"

def extract_text_pdf(pdf_path):

    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text("text")
        
        return text

def process_all_pdfs():

    for filename in os.listdir(DATA_FOL):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(DATA_FOL, filename)
            text = extract_text_pdf(pdf_path)

        #saving extracted text
        text_filename = filename.replace(".pdf",".txt")
        with open(os.path.join(OUTPUT_FOL, text_filename), "w", encoding="utf-8") as f:
            f.write(text)
        print(f" processed text from {filename}")

# Run the extraction
if __name__ == "__main__":
    process_all_pdfs()