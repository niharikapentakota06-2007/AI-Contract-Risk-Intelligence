# day4_fine_tune.py
from transformers import Trainer
from day3_model_config import get_model_and_args

def run_fine_tuning(train_dataset, eval_dataset):
    model, training_args = get_model_and_args("roberta-base", num_labels=2)
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )
    
    print("Starting Model Fine-Tuning on CUAD...")
    trainer.train()
    
    model.save_pretrained("./fine_tuned_legal_roberta")
    print("Model training complete and saved.")

if __name__ == "__main__":
    print("Fine-tuning pipeline prepared.")
