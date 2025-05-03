# Evaluation Folder

This folder contains scripts and notebooks for evaluating the performance of various models on sentiment analysis and intent classification tasks. The evaluations are conducted using datasets processed in the `extraction` folder.

## Contents

### Evaluation Scripts and Notebooks

1. **evaluate_sentiment_vader.ipynb**
   - Evaluates sentiment scores using the VADER sentiment analysis tool.
   - Maps VADER's compound score to a numerical scale from 1 to 5.
   - Saves predictions in the `results` directory.

2. **evaluate_sentiment.py**
   - Evaluates sentiment predictions from various models.
   - Compares predicted scores with actual scores to compute evaluation metrics.

3. **evaluate_intent.py**
   - Evaluates intent classification predictions from various models.
   - Compares predicted intents with actual intents to compute evaluation metrics.

### Results Directory

The `results` directory contains the output of the evaluation scripts and notebooks. It includes:

- **Sentiment Predictions**
  - `vader_sentiment_predictions.csv`: Predictions from the VADER sentiment analysis tool.
  - `combined_sentiment_predictions.csv`: Combined predictions from multiple models.
  - Model-specific sentiment predictions (e.g., `gemma3_sentiment_predictions.csv`, `llama3:8b_sentiment_predictions.csv`, etc.).

- **Intent Predictions**
  - Model-specific intent predictions (e.g., `mistral_intent_predictions.csv`, `deepseek-llm:7b_intent_predictions.csv`, etc.).

- **Metrics**
  - JSON files containing evaluation metrics for intent classification and sentiment analysis (e.g., `sentiment_metrics.json`, `mistral_intent_metrics.json`).

## How to Run Evaluations

1. **Sentiment Analysis**
   - To evaluate sentiment using VADER, open and execute the cells in `evaluate_sentiment_vader.ipynb`.
   - To evaluate sentiment predictions from other models, run `evaluate_sentiment.py` using the command:
     ```bash
     python evaluate_sentiment.py
     ```

2. **Intent Classification**
   - To evaluate intent predictions, run `evaluate_intent.py` using the command:
     ```bash
     python evaluate_intent.py
     ```

3. **Results**
   - All evaluation results will be saved in the `results` directory.
   - Use the CSV files to analyze individual predictions and the JSON files to review overall metrics.

## Prerequisites

- Install the required Python libraries using the command:
  ```bash
  pip install -r requirements.txt
  ```

- Ensure that the datasets are available in the `data/Cleaned_data` directory.

## Notes

- The evaluation scripts are designed to work with datasets processed in the `extraction` folder.
- Modify the paths in the scripts if the directory structure changes.