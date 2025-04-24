import os
import subprocess
import requests
from src.chatbot.processing import process_message

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

def is_ollama_running():
    """
    Check if the Ollama server is running.

    Returns:
        bool: True if the server is running, False otherwise.
    """
    try:
        response = requests.get("http://localhost:11434", timeout=2)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

def start_ollama():
    """
    Start the Ollama server if it is not running.
    """
    if not is_ollama_running():
        print("Starting Ollama server...")
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    start_ollama()  # Ensure Ollama is running
    model_name = "llama3:8b"
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    product_file = os.path.join(data_dir, "products.txt")

    product_list = load_product_list(product_file)

    if not product_list:
        print("Warning: Product list is empty. Proceeding without product filtering.")

    print("Welcome to the E-commerce Chatbot!")
    print("Type 'quit' to exit.")

    while True:
        user_input = input("> ")
        if user_input.lower() == "quit":
            break
        if user_input.strip():
            response = process_message(user_input, product_list, model_name)
            print(response)
            print()