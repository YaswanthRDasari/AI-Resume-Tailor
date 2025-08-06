from openai import OpenAI
import os
from dotenv import load_dotenv
from pypdf import PdfReader

# Explicitly load the .env from backend dir
env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")

print(f"[DEBUG] Loaded API KEY: {(api_key[:5]+'...') if api_key else 'None'} (length {len(api_key) if api_key else 0})")

if not api_key:
    raise ValueError("Missing OpenAI API key in .env file. Ensure OPENAI_API_KEY is set.")

client = OpenAI(
    api_key=api_key
)

def call_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def extract_text_from_pdf(file_stream):
    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_latex(file_stream):
    """
    Extracts plain text from a LaTeX file stream by removing LaTeX commands.
    """
    import re
    file_stream.seek(0)
    latex_content = file_stream.read().decode('utf-8')
    # Remove LaTeX comments
    latex_content = re.sub(r'%.*', '', latex_content)
    # Remove LaTeX commands
    text = re.sub(r'\\[a-zA-Z]+(\[[^\]]*\])?(\{[^\}]*\})?', '', latex_content)
    # Remove curly braces
    text = re.sub(r'[{}]', '', text)
    # Collapse multiple spaces/newlines
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
