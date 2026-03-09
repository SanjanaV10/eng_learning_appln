from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
import json
import os
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", ""))
print("haaaaaaa",os.environ.get("GOOGLE_API_KEY", ""))
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
    # Dummy data for now
    context = {'mistakes': []}
    return render(request, 'analysis.html')

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
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        try:
            # Force JSON response schema
            model = genai.GenerativeModel('gemini-1.5-flash', generation_config={"response_mime_type": "application/json"})
            prompt = f"""
            You are a strict but encouraging AI English tutor.
            The user said: "{user_message}"
            
            Instructions:
            1. Respond naturally to continue the conversation.
            2. If there is ANY grammar, spelling, or syntax mistake, you MUST provide a correction.
            
            Return ONLY a valid JSON object matching this schema:
            {{
                "response": "Your natural conversational reply corresponding to what they said.",
                "corrections": "Explain their mistake and provide the corrected sentence. If there are ABSOLUTELY NO mistakes, return 'None'."
            }}
            """
            chat_response = model.generate_content(prompt)
            result = json.loads(chat_response.text)
            
            bot_response = result.get('response', 'I understood.')
            corrections = result.get('corrections', 'None')
            
        except Exception as e:
            # Fallback for when API Key is missing or invalid
            bot_response = "I am currently running in offline mock mode since my AI brain is disconnected. But I can still check your grammar!"
            corrections = HeuristicCorrector.get_corrections(user_message)
        
        return JsonResponse({
            'response': bot_response,
            'corrections': corrections
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
