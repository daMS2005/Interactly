import os
import pandas as pd
import logging
from src.chatbot.processing import analyze_intent_and_ner, ollama

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def evaluate_intent_accuracy(df, product_list, model_name, output_dir):
    """
    Evaluate intent classification accuracy for a given model.

    Args:
        df (pd.DataFrame): DataFrame with "text" and "intent" columns.
        product_list (list[str]): List of valid product names.
        model_name (str): Name of the model to evaluate.
        output_dir (str): Directory to save intermediate results.

    Returns:
        pd.DataFrame: DataFrame with predictions (text, actual intent, predicted intent).
    """
    client = ollama.Client()
    predictions = []

    logging.info(f"Evaluating model '{model_name}' on {len(df)} samples.")

    for _, row in df.iterrows():
        user_message = row["text"]
        expected_intent = row["intent"]

        # Extract predicted intent
        analysis = analyze_intent_and_ner(client, user_message, product_list, model_name)
        predicted_intent = analysis.get("intent", "Other")

        # Append prediction to the list
        predictions.append({
            "text": user_message,
            "actual_intent": expected_intent,
            "predicted_intent": predicted_intent
        })

    # Convert predictions to a DataFrame
    predictions_df = pd.DataFrame(predictions)

    # Save intermediate results
    output_path = os.path.join(output_dir, f"{model_name}_predictions.csv")
    predictions_df.to_csv(output_path, index=False)
    logging.info(f"Predictions for model '{model_name}' saved to {output_path}")

    return predictions_df

def calculate_metrics(predictions_df):
    """
    Calculate accuracy metrics from predictions.

    Args:
        predictions_df (pd.DataFrame): DataFrame with predictions.

    Returns:
        dict: A dictionary with counts of correct/incorrect predictions per intent.
    """
    metrics = {"total": len(predictions_df), "correct": 0, "incorrect": 0, "per_intent": {}}

    for _, row in predictions_df.iterrows():
        actual_intent = row["actual_intent"]
        predicted_intent = row["predicted_intent"]

        if actual_intent not in metrics["per_intent"]:
            metrics["per_intent"][actual_intent] = {"correct": 0, "incorrect": 0}

        if actual_intent == predicted_intent:
            metrics["correct"] += 1
            metrics["per_intent"][actual_intent]["correct"] += 1
        else:
            metrics["incorrect"] += 1
            metrics["per_intent"][actual_intent]["incorrect"] += 1

    return metrics

def save_results(results, output_path):
    """
    Save evaluation results to a JSON file.

    Args:
        results (dict): Evaluation results.
        output_path (str): Path to save the results.
    """
    import json
    with open(output_path, "w") as f:
        json.dump(results, f, indent=4)
    logging.info(f"Results saved to {output_path}")

def load_dataset(csv_path):
    """
    Load dataset from a CSV file.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: DataFrame with the dataset.
    """
    return pd.read_csv(csv_path)

def load_product_list(filepath):
    """
    Load product names from a text file.

    Args:
        filepath (str): Path to the product list file.

    Returns:
        list[str]: List of product names.
    """
    try:
        with open(filepath, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return []

def main():
    """
    Main function to evaluate intent classification accuracy for multiple models.
    """
    # Load dataset
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(project_root, "data/Cleaned_data", "intent_dataset_sampled.csv")
    output_dir = os.path.join(project_root, "evaluation/results")
    os.makedirs(output_dir, exist_ok=True)

    df = load_dataset(dataset_path)

    # Ensure the dataset has the required columns
    if "text" not in df.columns or "intent" not in df.columns:
        raise ValueError("Dataset must contain 'text' and 'intent' columns.")

    # Log dataset statistics
    logging.info(f"Loaded dataset with {len(df)} samples.")
    intent_counts = df["intent"].value_counts().to_dict()
    logging.info(f"Intent distribution: {intent_counts}")

    # Define product list and models
    product_list = ["ProductA", "ProductB", "ProductC"]  # Products aren't used here - it's just a placeholder
    models = ["llama3:8b", "mistral", "deepseek"]

    # Evaluate each model and save results
    all_predictions = []
    all_metrics = {}
    for model_name in models:
        predictions_df = evaluate_intent_accuracy(df, product_list, model_name, output_dir)
        metrics = calculate_metrics(predictions_df)
        all_predictions.append(predictions_df)
        all_metrics[model_name] = metrics
        logging.info(f"Model: {model_name}, Accuracy: {metrics['correct'] / metrics['total']:.2%}")

    # Save combined predictions and metrics
    combined_predictions = pd.concat(all_predictions, ignore_index=True)
    combined_predictions_path = os.path.join(output_dir, "combined_predictions.csv")
    combined_predictions.to_csv(combined_predictions_path, index=False)
    logging.info(f"Combined predictions saved to {combined_predictions_path}")

    metrics_output_path = os.path.join(output_dir, "metrics.json")
    save_results(all_metrics, metrics_output_path)

if __name__ == "__main__":
    main()
