# day2_dataset.py
import torch
from torch.utils.data import Dataset

class LegalClauseDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

    def __len__(self):
        return len(self.labels)

if __name__ == "__main__":
    print("LegalClauseDataset class structure successfully initialized.")
