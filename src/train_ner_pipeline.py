import os
import subprocess
import spacy
from spacy.cli.init_config import init_config

def run_baseline_training(data_dir: str = "data/processed", output_dir: str = "output_model"):
    """
    Generates the required spaCy config file and executes the 
    baseline NER training loop.
    """
    config_path = os.path.join(data_dir, "base_config.cfg")
    full_config_path = os.path.join(data_dir, "config.cfg")
    train_data = os.path.join(data_dir, "train.spacy")
    
    # 1. Check if the prepared binary data from the previous script exists
    if not os.path.exists(train_data):
        raise FileNotFoundError(f"❌ '{train_data}' not found. Please run your 'train_baseline.py' script first!")

    print("⚙️ Step 1: Generating baseline spaCy configuration template...")
    # This automatically configures a lightweight CPU-optimized pipeline for NER
    init_config(
        lang="en", 
        pipeline=["ner"], 
        output_path=full_config_path, 
        optimize="efficiency"
    )
    print(f"✅ Configuration template generated at: {full_config_path}")

    # 2. Update config paths to point to your train.spacy dataset
    print("📝 Step 2: Injecting dataset paths into configuration file...")
    nlp = spacy.blank("en")
    config = nlp.config.from_disk(full_config_path)
    
    # Set training data paths dynamically
    config["paths"]["train"] = train_data
    config["paths"]["dev"] = train_data  # Using train as dev for the baseline test check
    config.to_disk(full_config_path)

    # 3. Trigger the training loop via subprocess
    print("🚀 Step 3: Launching spaCy training loop execution...")
    os.makedirs(output_dir, exist_ok=True)
    
    # This executes the official spaCy terminal training CLI directly from Python
    cmd = [
        "python", "-m", "spacy", "train", full_config_path,
        "--output", output_dir,
        "--nlp.batch_size", "128"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n🎉 Baseline model trained successfully! Model saved to: ./{output_dir}/model-best")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Training crashed or was interrupted: {str(e)}")

if __name__ == "__main__":
    run_baseline_training()
