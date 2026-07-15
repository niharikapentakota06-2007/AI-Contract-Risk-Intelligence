# day3_model_config.py
from transformers import AutoModelForSequenceClassification, TrainingArguments

def get_model_and_args(model_name="roberta-base", num_labels=2):
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)
    
    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True
    )
    
    return model, training_args

if __name__ == "__main__":
    model, args = get_model_and_args()
    print(f"Model loaded successfully. Output directory set to: {args.output_dir}")
