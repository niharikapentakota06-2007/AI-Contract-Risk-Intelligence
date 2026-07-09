import json
import os
import pandas as pd
from pathlib import Path

def parse_cuad_json(json_path: str, output_csv_path: str):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Raw CUAD file not found at {json_path}. Please download it first.")

    print(f"🔄 Reading raw CUAD dataset from {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    records = []
    
    for item in data.get('data', []):
        title = item.get('title', 'Unknown_Contract')
        for paragraph in item.get('paragraphs', []):
            context = paragraph.get('context', '')
            
            for qa in paragraph.get('qas', []):
                category = qa.get('id', 'Unknown_Category')
                answers = qa.get('answers', [])
                
                for ans in answers:
                    records.append({
                        "contract_title": title,
                        "text": context,
                        "category": category,
                        "answer_text": ans.get('text', ''),
                        "start_idx": ans.get('answer_start', 0),
                        "end_idx": ans.get('answer_start', 0) + len(ans.get('text', ''))
                    })
                    
    df = pd.DataFrame(records)
    df.drop_duplicates(subset=['text', 'category', 'start_idx', 'end_idx'], inplace=True)
    
    Path(output_csv_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv_path, index=False, encoding='utf-8')
    print(f"✅ Parsing complete! Saved {len(df)} records to: {output_csv_path}")

if __name__ == "__main__":
    parse_cuad_json("data/CUADv1.json", "data/processed/cuad_parsed.csv")
