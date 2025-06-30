from openai import OpenAI
import os
from dotenv import load_dotenv

# Explicitly load the .env from backend dir
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

print(f"[DEBUG] Loaded API KEY: {(api_key[:5]+'...') if api_key else 'None'} (length {len(api_key) if api_key else 0})")
print(f"[DEBUG] Loaded ENDPOINT: {endpoint if endpoint else 'None'}")


if not api_key or not endpoint:
    raise ValueError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT in .env!")

client = OpenAI(
    api_key=api_key,
    base_url=endpoint,
    default_headers={"api-key": api_key}
)

def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-35-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
