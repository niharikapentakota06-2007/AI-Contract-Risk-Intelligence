# day6_post_processing.py
import torch
import torch.nn.functional as F

def apply_confidence_threshold(logits, threshold=0.75):
    """
    Applies a strict threshold heuristic. If confidence is below the threshold, 
    mark as unclassified/uncertain (flagged for manual human review).
    """
    probabilities = F.softmax(torch.tensor(logits), dim=-1)
    max_probs, predictions = torch.max(probabilities, dim=-1)
    
    final_predictions = []
    for prob, pred in zip(max_probs, predictions):
        if prob.item() < threshold:
            final_predictions.append(-1) # -1 indicates "Uncertain / Requires Review"
        else:
            final_predictions.append(pred.item())
            
    return final_predictions, probabilities.tolist()

if __name__ == "__main__":
    sample_logits = [[0.2, 0.8], [0.45, 0.55]]
    preds, probs = apply_confidence_threshold(sample_logits)
    print(f"Processed predictions under high threshold: {preds}")
