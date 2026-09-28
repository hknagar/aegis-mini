from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()


def create_embedding(text: str):

    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
    )

    return result.embeddings[0].values