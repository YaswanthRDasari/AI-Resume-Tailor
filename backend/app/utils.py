from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from pypdf import PdfReader

# Explicitly load the .env from backend dir
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

print(f"[DEBUG] Loaded API KEY: {(api_key[:5]+'...') if api_key else 'None'} (length {len(api_key) if api_key else 0})")
print(f"[DEBUG] Loaded ENDPOINT: {endpoint if endpoint else 'None'}")
print(f"[DEBUG] Loaded DEPLOYMENT: {deployment if deployment else 'None'}")


if not api_key or not endpoint or not deployment or not api_version:
    raise ValueError("Missing Azure OpenAI credentials in .env file. Ensure AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_DEPLOYMENT, and AZURE_OPENAI_API_VERSION are set.")

client = AzureOpenAI(
    api_key=api_key,
    azure_endpoint=endpoint,
    api_version=api_version
)

def call_gpt(prompt):
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def extract_text_from_pdf(file_stream):
    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
