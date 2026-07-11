import os
import spacy
from spacy.tokens import DocBin
import pandas as pd
from tqdm import tqdm

def prepare_spacy_dataset(csv_path: str, output_spacy_path: str):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Missing dataset at {csv_path}. Run parser first.")
        
    print(f"📦 Loading structured dataset from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    nlp = spacy.blank("en")
    doc_bin = DocBin()
    
    print("🏷️ Re-aligning contract annotations into spaCy spans...")
    for _, row in tqdm(df.iterrows(), total=df.shape[0]):
        text = str(row['text'])
        start = int(row['start_idx'])
        end = int(row['end_idx'])
        
        raw_label = str(row['category']).upper().replace(" ", "_").replace("-", "_")
        clean_label = raw_label[:15] 
        
        doc = nlp.make_doc(text)
        entities = []
        
        span = doc.char_span(start, end, label=clean_label, alignment_mode="contract")
        if span is not None:
            entities.append(span)
            try:
                doc.ents = entities
                doc_bin.add(doc)
            except ValueError:
                continue
                
    doc_bin.to_disk(output_spacy_path)
    print(f"💾 Binary data stream generated at: {output_spacy_path}")
    print("\n🚀 Ready for spaCy baseline CLI. Run the following command next:")
    print(f"   python -m spacy train config.cfg --output ./output_model --paths.train {output_spacy_path} --paths.dev {output_spacy_path}")

if __name__ == "__main__":
    prepare_spacy_dataset("data/processed/cuad_parsed.csv", "data/processed/train.spacy")
