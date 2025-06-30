import os
from dotenv import load_dotenv

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '.env'))
print(f"Loading .env from: {env_path}")

load_dotenv(dotenv_path=env_path)

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

print("API KEY:", api_key)
print("ENDPOINT:", endpoint)
