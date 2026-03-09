import os
import json
import openai
from dotenv import load_dotenv

load_dotenv(dotenv_path="core/.env")

client = openai.OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ.get("GITHUB_TOKEN"),
)

def test_hi():
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a strict but encouraging AI English tutor and translator. "
                        "Instructions:\n"
                        "1. If the user's message is in a language OTHER THAN English, you MUST provide the English translation first.\n"
                        "2. Then, respond naturally in English to keep the conversation going.\n"
                        "3. If the user attempts English but makes grammar, spelling, or syntax mistakes, you MUST provide a detailed correction.\n"
                        "4. If no translation is needed (user spoke English), set translation to 'None'. If no corrections are needed, set corrections to 'None'.\n\n"
                        "Return ONLY a valid JSON object matching this schema:\n"
                        "{\n"
                        "  \"translation\": \"Wait! You said it in your native language. In English, that is: [Translation]\",\n"
                        "  \"response\": \"Your conversational reply in English.\",\n"
                        "  \"corrections\": \"Textual feedback on the user's English (original or translation).\"\n"
                        "}"
                    )
                },
                {
                    "role": "user",
                    "content": "hi"
                }
            ],
            model="gpt-4o-mini",
            response_format={"type": "json_object"}
        )
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_hi()
