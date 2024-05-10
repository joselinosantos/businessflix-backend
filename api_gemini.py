import google.generativeai as genai
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Obtém a API_KEY do arquivo .env
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Verifica se a API_KEY foi encontrada
if GOOGLE_API_KEY is None:
    raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")

# Configura o genai com a API_KEY
genai.configure(api_key=GOOGLE_API_KEY)
