import torch
import pandas as pd
from transformers import BertTokenizerFast

def analyze_features():
    # Initialize tokenizer (must match what you used originally)
    tokenizer = BertTokenizerFast.from_pretrained('bert-base-cased')
    
    # =====================
    # 1. NER Dataset Analysis
    # =====================
    print("="*40)
    print("NER DATASET FEATURES")
    print("="*40)

    try:
        # Load NER tensors
        ner_input_ids = torch.load('Cleaned_Data/NER/input_ids.pt')
        ner_labels = torch.load('Cleaned_Data/NER/labels.pt')

        # Basic stats
        print(f"\nShape of input_ids: {ner_input_ids.shape}")
        print(f"Shape of labels: {ner_labels.shape}\n")

        # Token analysis
        sample_tokens = tokenizer.convert_ids_to_tokens(ner_input_ids[0].tolist())
        print(f"Sample tokenized text (first 10 tokens):\n{sample_tokens[:10]}\n")

        # Label distribution
        unique_labels, counts = torch.unique(ner_labels, return_counts=True)
        label_counts = dict(zip(unique_labels.tolist(), counts.tolist()))
        total_labels = sum(label_counts.values())
        print("Label distribution:")
        label_names = {0: 'O (non-entity)', 1: 'B (entity start)', 2: 'I (entity continuation)'}
        for label_id, count in label_counts.items():
            print(f"  {label_names.get(label_id, f'Unknown {label_id}')}: {count} tokens ({count/total_labels:.1%})")

    except Exception as e:
        print(f"\nError analyzing NER data: {e}")

    # =====================
    # 2. Customer Intent Analysis
    # =====================
    print("\n" + "="*40)
    print("CUSTOMER INTENT DATASET")
    print("="*40)

    try:
        # Load customer dataset
        df = pd.read_csv('Cleaned_Data/Customer_Service_Training_Dataset_Final.csv')

        # Basic stats
        print(f"\nTotal samples: {len(df)}")
        print(f"Sequence length: {len(eval(df['input_ids'].iloc[0]))} tokens\n")

        # Intent distribution (reverse map labels if available)
        intent_counts = df['intent_label'].value_counts().sort_index()
        print("Intent label distribution:")
        print(intent_counts.to_string())
        print(f"\nTotal unique intents: {len(intent_counts)}")

        # Input example
        sample_input = eval(df['input_ids'].iloc[0])[:10]  # First 10 token IDs
        sample_text = tokenizer.decode(sample_input)
        print(f"\nSample input (first 10 tokens):\n{sample_text}")

    except Exception as e:
        print(f"\nError analyzing Customer Intent data: {e}")

if __name__ == "__main__":
    analyze_features()