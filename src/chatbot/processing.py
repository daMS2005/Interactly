import ollama
import json

def analyze_intent_and_ner(client, user_message, product_list, model_name):
    """
    Analyze user message for intent and extract product names.

    Args:
        client (ollama.Client): Ollama client instance.
        user_message (str): The user's message.
        product_list (list[str]): List of valid product names.
        model_name (str): Name of the model to use.

    Returns:
        dict: A dictionary with intent and filtered product names.
    """
    prompt = f"""Analyze the following message for intent and product mentions. 
    Intent categories: Refund, Payment, Feedback, Contact, Other.
    Products: {', '.join(product_list)}.
    Respond in JSON format: {{"intent": "category", "products": ["product1", "product2"]}}.
    Do not include any other text besides the JSON.

    Message: {user_message}
    """
    response = client.generate(prompt=prompt, model=model_name)
    
    try:
        result = json.loads(response.response.strip())
        result["products"] = [p for p in result.get("products", []) if p in product_list]
        return result
    except json.JSONDecodeError:
        return {"intent": "Other", "products": []}

def analyze_sentiment(client, user_message, products, model_name):
    """
    Analyze sentiment and return a numerical score between 1 and 5.

    Args:
        client (ollama.Client): Ollama client instance.
        user_message (str): The user's message.
        products (list[str]): List of products mentioned.
        model_name (str): Name of the model to use.

    Returns:
        float: Sentiment score (1 to 5) or None.
    """

    prompt = f"""
    Analyze the sentiment of the following feedback message.
    Message: {user_message}
    Respond with a json object containing a single key "score" with a value between 1 and 5.
    The score should reflect the sentiment of the message, where 1 is very negative and 5 is very positive.
    Do not include any other text besides the JSON.
    """
    response = client.generate(prompt=prompt, model=model_name)
    # Extract the score from the response
    try:
        result = json.loads(response.response.strip())
        return int(result.get("score", 0))
    except (json.JSONDecodeError, ValueError):
        return None

def generate_response(client, user_message, intent, products, sentiment, model_name):
    """
    Generate a chatbot response based on the analysis.

    Args:
        client (ollama.Client): Ollama client instance.
        user_message (str): The user's message.
        intent (str): Identified intent.
        products (list[str]): List of products mentioned.
        sentiment (str): Sentiment analysis result.
        model_name (str): Name of the model to use.

    Returns:
        str: The chatbot's response.
    """
    prompt = f"""
    Generate a response based on the following details:
    Intent: {intent}
    Products: {', '.join(products)}
    Sentiment: {sentiment}
    Original Message: {user_message}
    Ensure the response is helpful and professional.
    The response is passed directly to the user, so do not include any additional instructions or context.
    """
    response = client.generate(prompt=prompt, model=model_name)
    return response.response.strip()

def process_message(user_message, product_list, model_name):
    """
    Orchestrate the chatbot processing pipeline.

    Args:
        user_message (str): The user's message.
        product_list (list[str]): List of valid product names.
        model_name (str): Name of the model to use.

    Returns:
        str: Final chatbot response.
    """
    client = ollama.Client()
    analysis = analyze_intent_and_ner(client, user_message, product_list, model_name)
    intent = analysis.get("intent", "Other")
    products = analysis.get("products", [])

    sentiment = None
    if intent == "Feedback":
        sentiment = analyze_sentiment(client, user_message, products, model_name)

    return generate_response(client, user_message, intent, products, sentiment, model_name)
