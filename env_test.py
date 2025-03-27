from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="/Users/danielmora/Interactly/.env")

print("API_KEY:", os.getenv("API_KEY"))
print("API_SECRET:", os.getenv("API_SECRET"))
