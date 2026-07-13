# day1_tokenization.py
import json
from transformers import AutoTokenizer

def load_data(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def tokenize_dataset(data, tokenizer_name="roberta-base", max_length=512):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    
    texts = [item['text'] for item in data]
    labels = [item['label'] for item in data] # Classifying complex legal clauses
    
    tokenized_inputs = tokenizer(
        texts, 
        truncation=True, 
        padding="max_length", 
        max_length=max_length,
        return_tensors="pt"
    )
    
    return tokenized_inputs, labels

if __name__ == "__main__":
    # Example usage with placeholder path
    # sample_data = [{"text": "This Agreement is made on...", "label": 1}]
    print("Initializing tokenizer for RoBERTa...")
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    print("Tokenizer ready for legal clause processing.")
