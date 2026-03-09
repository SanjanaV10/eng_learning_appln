from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import UserInteraction
import json
import os
import openai
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: Path(__file__).resolve().parent
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

# Configure GitHub Copilot (via OpenAI SDK)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
if not GITHUB_TOKEN:
    print("WARNING: GITHUB_TOKEN is not set. AI features will fallback to mock mode.")

client = openai.OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=GITHUB_TOKEN,
)

def home(request):
    return render(request, 'home.html')

@login_required
def conversation(request):
    return render(request, 'conversation.html')

@login_required
def games(request):
    return render(request, 'games.html')

@login_required
def game_vocab_match(request):
    return render(request, 'game_vocab.html')

@login_required
def game_fill_blanks(request):
    return render(request, 'game_blanks.html')

@login_required
def game_memory(request):
    return render(request, 'game_memory.html')

@login_required
def quizzes(request):
    return render(request, 'quizzes.html')

@login_required
def analysis(request):
    interactions = UserInteraction.objects.filter(user=request.user).order_by('-timestamp')
    
    total_conversations = interactions.count()
    mistakes = interactions.filter(is_mistake=True)
    total_mistakes = mistakes.count()
    
    # Calculate accuracy
    if total_conversations > 0:
        accuracy = int(((total_conversations - total_mistakes) / total_conversations) * 100)
    else:
        accuracy = 0
        
    context = {
        'total_conversations': total_conversations,
        'accuracy': accuracy,
        'mistakes_fixed': total_mistakes,
        'mistakes': interactions.filter(is_mistake=True)[:10], # Show last 10 mistakes
    }
    return render(request, 'analysis.html', context)

class HeuristicCorrector:
    @staticmethod
    def get_corrections(text):
        if not text:
            return "None"
        
        corrections = []
        original = text.strip()
        
        # 1. Capitalization check
        if not original[0].isupper():
            corrections.append("The first letter of your sentence should be capitalized.")
        
        # 2. Punctuation check
        if original[-1] not in ('.', '!', '?'):
            corrections.append("Remember to end your sentence with a period, exclamation mark, or question mark.")
        
        # 3. Common 'i' to 'I'
        import re
        if re.search(r'\bi\b', original):
            corrections.append("The word 'I' should always be capitalized when referring to yourself.")
            
        # 4. Common contraction missing apostrophe
        missing_apostrophes = {
            r"\bdont\b": "don't",
            r"\bim\b": "I'm",
            r"\bcant\b": "can't",
            r"\bwont\b": "won't",
            r"\biv\b": "I've",
            r"\byoure\b": "you're"
        }
        for pattern, fix in missing_apostrophes.items():
            if re.search(pattern, original.lower()):
                corrections.append(f"Use an apostrophe for '{fix}'.")
        
        # 5. Simple Subject-Verb Agreement (He/She/It + base verb)
        # Very limited but catches high-frequency errors
        third_person_mistakes = {
            r"\b(he|she|it) go\b": "goes",
            r"\b(he|she|it) want\b": "wants",
            r"\b(he|she|it) like\b": "likes",
            r"\b(he|she|it) say\b": "says"
        }
        for pattern, fix in third_person_mistakes.items():
            if re.search(pattern, original.lower()):
                corrections.append(f"Use the third-person singular verb '{fix}'.")

        if not corrections:
            return "None"
        
        return " | ".join(corrections)

def api_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            print(f"DEBUG: Received message: {user_message}")
            
            if not GITHUB_TOKEN:
                raise ValueError("No API Token")

            # Using Copilot (GitHub Models)
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a strict but encouraging AI English tutor and translator. "
                            "Instructions:\n"
                            "1. If the user's message is in a language OTHER THAN English (e.g., Hindi, Spanish, etc.), you MUST detect the language.\n"
                            "2. If translation is needed, provide it in the 'translation' field as: 'I noticed you're speaking in [Language]. In English, that is: [Full English Translation]'.\n"
                            "3. Then, respond naturally in English to keep the conversation going.\n"
                            "4. If the user attempts English but has grammar, spelling, or syntax mistakes, you MUST provide a detailed correction in the 'corrections' field.\n"
                            "5. If the message is already perfect English, set translation and corrections to 'None'.\n\n"
                            "Return ONLY a valid JSON object matching this schema:\n"
                            "{\n"
                            "  \"translation\": \"[The learning-focused translation hint]\",\n"
                            "  \"response\": \"Your conversational reply in English.\",\n"
                            "  \"corrections\": \"Textual feedback on the user's English usage.\"\n"
                            "}"
                        )
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ],
                model="gpt-4o-mini",
                response_format={"type": "json_object"}
            )
            
            raw_content = response.choices[0].message.content
            print(f"DEBUG: Raw AI Response: {raw_content}")
            result = json.loads(raw_content)

            bot_response = result.get('response', 'I understood.')
            corrections = result.get('corrections', 'None')
            translation = result.get('translation', 'None')
            
        except Exception as e:
            print(f"DEBUG: AI Error: {str(e)}")
            # Fallback
            bot_response = "I am currently running in offline mock mode since my AI brain is disconnected. But I can still check your grammar!"
            if 'user_message' in locals():
                corrections = HeuristicCorrector.get_corrections(user_message)
            else:
                corrections = "Error processing request."
            translation = "None"

        # Save the interaction for analysis
        try:
            is_mistake = (corrections != "None" and corrections != "")
            UserInteraction.objects.create(
                user=request.user,
                user_text=user_message,
                ai_response=bot_response,
                corrections=corrections,
                is_mistake=is_mistake
            )
        except Exception as save_error:
            print(f"DEBUG: Failed to save interaction: {str(save_error)}")

        return JsonResponse({
            'response': bot_response,
            'corrections': corrections,
            'translation': translation
        })
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    return render(request, 'logout_confirm.html')
