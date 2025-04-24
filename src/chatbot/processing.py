import ollama
import json
import os
import streamlit as st

def load_product_catalog():
    """Load the product catalog from JSON file."""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data")
    catalog_file = os.path.join(data_dir, "product_catalog.json")
    
    try:
        with open(catalog_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"stores": []}

def get_store_details(store_name, catalog):
    """Get detailed information about a specific store."""
    for store in catalog["stores"]:
        if store["name"].lower() == store_name.lower():
            return store
    return None

def get_product_details(store_name, product_name, catalog):
    """Get detailed information about a specific product within a store."""
    store = get_store_details(store_name, catalog)
    if store:
        for product in store["products"]:
            if product["name"].lower() == product_name.lower():
                return product
    return None

def analyze_intent_and_ner(client, user_message, store_name, product_name, model_name):
    """
    Analyze user message for intent and context.

    Args:
        client (ollama.Client): Ollama client instance.
        user_message (str): The user's message.
        store_name (str): Selected store name.
        product_name (str): Selected product name.
        model_name (str): Name of the model to use.

    Returns:
        dict: A dictionary with intent and context information.
    """
    # Check store type
    store_name_lower = store_name.lower() if store_name else ""
    is_dr_squatch = "dr. squatch" in store_name_lower
    is_techgear = "techgear" in store_name_lower
    is_bloom = "bloom" in store_name_lower
    is_urban = "urban" in store_name_lower
    
    # Add store-specific context
    store_context = ""
    if is_dr_squatch:
        store_context = """
        This is a Dr. Squatch store, which sells natural, manly soaps and personal care products.
        Dr. Squatch products are known for their natural ingredients, manly scents, and humorous marketing.
        Common product categories include soaps, shampoos, conditioners, deodorants, and hair care products.
        The brand targets young men and emphasizes natural ingredients and manliness.
        """
    elif is_techgear:
        store_context = """
        This is a TechGear store, which sells high-performance fitness and technology products.
        TechGear products are known for their durability, advanced features, and integration of tech with fitness.
        Common product categories include smartwatches, fitness trackers, workout equipment, and tech accessories.
        The brand targets fitness enthusiasts and tech-savvy individuals who want to optimize their workouts.
        """
    elif is_bloom:
        store_context = """
        This is a Bloom Flower Shop, which sells elegant floral arrangements and garden supplies.
        Bloom products are known for their beauty, freshness, and artistic design.
        Common product categories include bouquets, arrangements, potted plants, garden tools, and floral accessories.
        The brand targets individuals who appreciate beauty, elegance, and the natural world.
        """
    elif is_urban:
        store_context = """
        This is an Urban Outfitters store, which sells trendy clothing, accessories, and home goods.
        Urban Outfitters products are known for their contemporary style, unique designs, and urban aesthetic.
        Common product categories include clothing, accessories, home decor, beauty products, and lifestyle items.
        The brand targets young, fashion-conscious individuals who value style and self-expression.
        """
    
    prompt = f"""Analyze the following message for intent and context. 
    Intent categories: Product Inquiry, Store Information, Feedback, Technical Support, Delivery, Pricing, Other.
    Store: {store_name}
    Product: {product_name}
    {store_context}
    Respond in JSON format: {{"intent": "category", "context": "relevant details"}}.
    Do not include any other text besides the JSON.

    Message: {user_message}
    """
    response = client.generate(prompt=prompt, model=model_name)
    
    try:
        return json.loads(response.response.strip())
    except json.JSONDecodeError:
        return {"intent": "Other", "context": ""}

def analyze_sentiment(client, user_message, model_name):
    """
    Analyze sentiment and return a numerical score between 1 and 5.

    Args:
        client (ollama.Client): Ollama client instance.
        user_message (str): The user's message.
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
    try:
        result = json.loads(response.response.strip())
        return int(result.get("score", 0))
    except (json.JSONDecodeError, ValueError):
        return None

def generate_response(client, user_message, store_name, product_name, intent, context, sentiment, model_name, catalog):
    """
    Generate a chatbot response based on the analysis.

    Args:
        client (ollama.Client): Ollama client instance.
        user_message (str): The user's message.
        store_name (str): Selected store name.
        product_name (str): Selected product name.
        intent (str): Identified intent.
        context (str): Additional context from analysis.
        sentiment (int): Sentiment score (1-5).
        model_name (str): Name of the model to use.
        catalog (dict): Product catalog with detailed information.

    Returns:
        str: The chatbot's response.
    """
    # Get store and product details
    store_details = get_store_details(store_name, catalog)
    product_details = get_product_details(store_name, product_name, catalog) if product_name else None
    
    # Determine tone based on store
    store_name_lower = store_name.lower() if store_name else ""
    is_dr_squatch = "dr. squatch" in store_name_lower
    is_techgear = "techgear" in store_name_lower
    is_bloom = "bloom" in store_name_lower
    is_urban = "urban" in store_name_lower
    
    # Construct a rich context for the LLM
    context_str = f"""
    Store: {store_name}
    Product: {product_name if product_name else 'All Products'}
    User Intent: {intent}
    Additional Context: {context}
    Sentiment: {sentiment if sentiment else 'Not analyzed'}
    Original Message: {user_message}
    """
    
    # Add store details if available
    if store_details:
        context_str += f"""
        Store Details:
        - Description: {store_details['description']}
        - Features: {', '.join(store_details['features'])}
        - Target Audience: {', '.join(store_details['target_audience'])}
        - Location: {store_details['location']['address']}
        
        Available Products:
        """
        # Add all products from the store
        for product in store_details['products']:
            context_str += f"""
            {product['name']}:
            - Category: {product['category']}
            - Price: ${product['price']}
            - Description: {product['description']}
            - Key Features: {', '.join(product['features'])}
            """
    
    # Add focused product details if a specific product is selected
    if product_details:
        context_str += f"""
        Selected Product Details:
        - Name: {product_details['name']}
        - Category: {product_details['category']}
        - Price: ${product_details['price']}
        - Description: {product_details['description']}
        - Features: {', '.join(product_details['features'])}
        - Target Audience: {', '.join(product_details['target_audience'])}
        - Common Concerns: {', '.join(product_details['common_concerns'])}
        """
    
    # Add conversation history for context awareness
    if hasattr(st.session_state, 'messages') and st.session_state.messages:
        context_str += "\nPrevious Conversation:\n"
        # Add last 5 messages for context
        for msg in st.session_state.messages[-5:]:
            context_str += f"{msg['role'].title()}: {msg['content']}\n"
    
    # Add tone instructions based on store
    tone_instructions = ""
    if is_dr_squatch:
        tone_instructions = """
        You are a laid-back, youngster-friendly customer service assistant for Dr. Squatch.
        Use a casual, relaxed tone with lots of slang and youth-oriented language.
        Be enthusiastic, use emojis, and make references to popular culture.
        Avoid formal language and corporate speak.
        Make the customer feel like they're talking to a cool friend who knows all about Dr. Squatch products.
        """
    elif is_techgear:
        tone_instructions = """
        You are a super manly, gym bro customer service assistant for TechGear Pro.
        Use a very masculine, energetic tone with lots of gym and fitness references.
        Be enthusiastic about technology and fitness, using terms like "bro", "dude", "gains", "pump", etc.
        Make references to lifting weights, working out, and being strong.
        Use phrases like "let's crush this", "get those gains", and "level up your tech game".
        Be confident, assertive, and motivational in your responses.
        Make the customer feel like they're talking to a tech-savvy gym enthusiast.
        """
    elif is_bloom:
        tone_instructions = """
        You are a posh, feminine customer service assistant for Blooming Flowers.
        Use an elegant, refined tone with lots of floral and aesthetic references.
        Be graceful, sophisticated, and detail-oriented in your responses.
        Use phrases like "darling", "lovely", "beautiful", and "exquisite".
        Make references to flowers, gardens, and elegant aesthetics.
        Be warm and welcoming, but maintain a sense of sophistication.
        Make the customer feel like they're talking to a knowledgeable florist with impeccable taste.
        """
    elif is_urban:
        tone_instructions = """
        You are a casual, feminine customer service assistant for Urban Style Co.
        Use a friendly, laid-back tone with a touch of feminine energy.
        Be approachable, trendy, and knowledgeable about fashion and lifestyle.
        Use phrases like "totally", "for sure", "love it", and "so cute".
        Make references to current trends, fashion, and urban lifestyle.
        Be helpful and informative while maintaining a casual, friendly demeanor.
        Make the customer feel like they're talking to a stylish friend who knows all about the latest trends.
        """
    else:
        tone_instructions = """
        You are a helpful customer service assistant.
        Use a professional, friendly tone.
        Be informative and helpful.
        """
    
    prompt = f"""
    {tone_instructions}
    
    Based on the following context, provide a helpful, tailored response.
    Consider the user's intent, sentiment, and any product/store details provided.
    Remember the conversation history and maintain continuity in your responses.
    
    Context:
    {context_str}
    
    Provide a response that:
    1. Addresses the user's specific question or concern
    2. References relevant store/product details when appropriate
    3. Offers additional helpful information based on the store's target audience and features
    4. Maintains the appropriate tone for the store
    5. Includes specific details from the store/product information when relevant
    6. Shows awareness of the conversation history and maintains continuity
    7. If discussing products, feel free to mention other relevant products from the store
    
    The response should be direct and helpful, without any additional instructions or context.
    """
    
    response = client.generate(prompt=prompt, model=model_name)
    return response.response.strip()

def process_message(user_message, store_name, product_name=None, model_name="llama3:8b"):
    """
    Orchestrate the chatbot processing pipeline.

    Args:
        user_message (str): The user's message.
        store_name (str): Selected store name.
        product_name (str, optional): Selected product name.
        model_name (str): Name of the model to use.

    Returns:
        str: Final chatbot response.
    """
    client = ollama.Client()
    
    # Load product catalog
    catalog = load_product_catalog()
    
    # Analyze intent and context
    analysis = analyze_intent_and_ner(client, user_message, store_name, product_name, model_name)
    intent = analysis.get("intent", "Other")
    context = analysis.get("context", "")

    # Analyze sentiment for feedback
    sentiment = None
    if intent == "Feedback":
        sentiment = analyze_sentiment(client, user_message, model_name)

    # Generate tailored response
    return generate_response(client, user_message, store_name, product_name, intent, context, sentiment, model_name, catalog)
