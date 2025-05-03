# Interactly - AI Customer Service

Interactly is an AI-powered customer service assistant designed to provide tailored responses to user queries. It supports sentiment analysis, intent classification, and personalized responses based on store and product details.

## Features
- Chatbot interface for interacting with customers.
- Sentiment analysis and intent classification using advanced language models.
- Store and product-specific responses with tailored tones.
- Evaluation scripts for analyzing model performance.

## Prerequisites

1. **Python Environment**
   - Install Python 3.9 or higher.
   - Install required libraries using the command:
     ```bash
     pip install -r requirements.txt
     ```

2. **Ollama Setup**
   - Install the Ollama client from [Ollama's official website](https://ollama.ai/).
   - Ensure the following models are installed:
     - `llama3:7b` (required for chatbot functionality).
     - `mistral` (only required for intent evaluation).
     - `deepseek-llm:7b` (only required for sentiment evaluation).
   - Use the command below to install a model:
     ```bash
     ollama pull <model_name>
     ```

## Running the Project

1. **Start the Streamlit App**
   - Run the following command to start the chatbot interface:
     ```bash
     streamlit run streamlit_app.py
     ```
   - Open the provided URL in your browser to interact with the chatbot.

2. **Chatbot Functionality**
   - Select a store and product from the sidebar.
   - Enter your query in the chat input box.
   - The chatbot will provide tailored responses based on the selected store and product.

## Running Evaluations
1. **Sentiment Analysis Evaluation**
   - Open and execute the `evaluate_sentiment_vader.ipynb` notebook to evaluate sentiment using VADER.
   - Run the `evaluate_sentiment.py` script for model-based sentiment evaluation:
     ```bash
     python evaluation/evaluate_sentiment.py
     ```

2. **Intent Classification Evaluation**
   - Run the `evaluate_intent.py` script for intent evaluation:
     ```bash
     python evaluation/evaluate_intent.py
     ```

3. **Model Requirements for Evaluations**
   - Ensure the following models are installed:
     - `llama3:7b`
     - `mistral`
     - `deepseek-llm:7b`

## Notes
- The chatbot requires only the `llama3:7b` model for operation.
- Evaluation scripts require additional models (`mistral` and `deepseek-llm:7b`).
- Ensure datasets are available in the `data/Cleaned_data` directory for evaluations.