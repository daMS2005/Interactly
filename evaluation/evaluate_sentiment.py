import os
import pandas as pd
import logging
from src.chatbot.processing import analyze_sentiment, ollama

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(asctime)s - %(message)s")

def check_ollama_running():
    """
    Check if the Ollama service is running.

    Raises:
        RuntimeError: If Ollama is not running.
    """
    try:
        client = ollama.Client()
        client.generate(prompt="ping", model="llama3:8b")  # Test with a simple prompt
        logging.info("Ollama service is running.")
    except Exception as e:
        raise RuntimeError("Ollama service is not running. Please start the service and try again.") from e

def evaluate_sentiment_accuracy(df, model_name, output_dir):
    """
    Evaluate sentiment analysis accuracy for a given model.

    Args:
        df (pd.DataFrame): DataFrame with "Text" and "Score" columns where Score is between 1 and 5.
        model_name (str): Name of the model to evaluate.
        output_dir (str): Directory to save intermediate results.

    Returns:
        pd.DataFrame: DataFrame with predictions (text, actual_score, predicted_score) where scores are between 1 and 5.
    """
    client = ollama.Client()
    predictions = []
    logging.info(f"Evaluating sentiment analysis with model '{model_name}' on {len(df)} samples.")
    for _, row in df.iterrows():
        user_message = row["Text"]
        actual_score = row["Score"]  # actual score in the range 1-5
        # Extract predicted sentiment score (1-5)
        predicted_score = analyze_sentiment(client, user_message, ["ProductA"], model_name)
        
        if predicted_score is not None:
            predicted_score = int(predicted_score)
                
        predictions.append({
            "text": user_message,
            "actual_score": actual_score,
            "predicted_score": predicted_score
        })
        print(model_name, actual_score, predicted_score)

    # Convert predictions to a DataFrame
    predictions_df = pd.DataFrame(predictions)

    # Save intermediate results
    output_path = os.path.join(output_dir, f"{model_name}_sentiment_predictions.csv")
    predictions_df.to_csv(output_path, index=False)
    logging.info(f"Sentiment predictions for model '{model_name}' saved to {output_path}")

    return predictions_df

def calculate_sentiment_metrics(predictions_df):
    """
    Calculate accuracy metrics from sentiment predictions.

    Args:
        predictions_df (pd.DataFrame): DataFrame with predictions where both actual_score and predicted_score are in [1,5].

    Returns:
        dict: A dictionary with counts of exact correct predictions.
    """
    metrics = {"total": len(predictions_df), "correct": 0, "incorrect": 0}
    for _, row in predictions_df.iterrows():
        actual = row["actual_score"]
        predicted = row["predicted_score"]
        if actual == predicted:
            metrics["correct"] += 1
        else:
            metrics["incorrect"] += 1
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

def main():
    """
    Main function to evaluate sentiment analysis accuracy for multiple models.
    """
    # Check if Ollama is running
    check_ollama_running()

    # Load dataset
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(project_root, "data/Cleaned_data", "sentiment_analysis.csv")
    output_dir = os.path.join(project_root, "evaluation/results")
    os.makedirs(output_dir, exist_ok=True)

    df = load_dataset(dataset_path)

    print(df.head())

    # Ensure the dataset has the required columns
    if "Text" not in df.columns or "Score" not in df.columns:
        raise ValueError("Dataset must contain 'Text' and 'Score' columns.")

    # Log dataset statistics
    logging.info(f"Loaded dataset with {len(df)} samples.")

    # Define models
    models = ["llama3:8b", "deepseek-llm:7b", "mistral"]

    sample_text = "Several years ago I purchased these moth traps and they were filled in a matter of days.  I received these a few weeks ago and they have remained empty with the moths flying nearby.  I suppose like everything else - they changed the formula or something.  Soooooo disappointed."
    sample_prediction = analyze_sentiment(ollama.Client(), sample_text, ["ProductA"], "llama3:8b")
    print(f"Sample prediction for text: {sample_text}\nPredicted sentiment score: {sample_prediction}")


    # Evaluate each model and save results
    all_predictions = []
    all_metrics = {}
    for model_name in models:
        predictions_df = evaluate_sentiment_accuracy(df, model_name, output_dir)
        metrics = calculate_sentiment_metrics(predictions_df)
        all_predictions.append(predictions_df)
        all_metrics[model_name] = metrics
        logging.info(f"Model: {model_name}, Accuracy: {metrics['correct'] / metrics['total']:.2%}")

    # Save combined predictions and metrics
    combined_predictions = pd.concat(all_predictions, ignore_index=True)
    combined_predictions_path = os.path.join(output_dir, "combined_sentiment_predictions.csv")
    combined_predictions.to_csv(combined_predictions_path, index=False)
    logging.info(f"Combined sentiment predictions saved to {combined_predictions_path}")

    metrics_output_path = os.path.join(output_dir, "sentiment_metrics.json")
    save_results(all_metrics, metrics_output_path)

if __name__ == "__main__":
    main()
