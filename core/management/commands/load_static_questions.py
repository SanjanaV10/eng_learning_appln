from django.core.management.base import BaseCommand
from core.models import Question
import json

class Command(BaseCommand):
    help = 'Loads static questions into the database'

    def handle(self, *args, **kwargs):
        # 1. Quizzes
        quiz_data = [
            {
                "question": "Choose the correct sentence:",
                "options": ["She don't like apples.", "She doesn't likes apples.", "She doesn't like apples.", "She not like apples."],
                "correct": 2,
                "explanation": "'Doesn't' is the correct auxiliary for third-person singular, and the main verb ('like') remains in its base form."
            },
            {
                "question": "If it rains tomorrow, I ___ at home.",
                "options": ["will stay", "would stay", "stayed", "staying"],
                "correct": 0,
                "explanation": "This is a First Conditional sentence, which uses 'will + base verb' in the result clause."
            },
            {
                "question": "Identify the synonym for 'Abundant':",
                "options": ["Scarce", "Plentiful", "Empty", "Brief"],
                "correct": 1,
                "explanation": "'Abundant' means existing or available in large quantities; 'Plentiful' is its direct synonym."
            },
            {
                "question": "I have been waiting here ___ exactly two hours.",
                "options": ["since", "for", "from", "during"],
                "correct": 1,
                "explanation": "Use 'for' with a duration of time (two hours). Use 'since' with a point in time (e.g., since 2 PM)."
            },
            {
                "question": "By this time next year, she ___ her degree.",
                "options": ["finishes", "will finish", "will have finished", "is finishing"],
                "correct": 2,
                "explanation": "The Future Perfect tense ('will have finished') is used to express an action that will be completed before a specified time in the future."
            }
        ]

        # 2. Vocab Match
        vocab_data = [
            { "word": 'Abundant', "meaning": 'Existing or available in large quantities; plentiful.' },
            { "word": 'Diligent', "meaning": 'Having or showing care and conscientiousness in one\'s work or duties.' },
            { "word": 'Eloquent', "meaning": 'Fluent or persuasive in speaking or writing.' },
            { "word": 'Inevitable', "meaning": 'Certain to happen; unavoidable.' },
            { "word": 'Lucrative', "meaning": 'Producing a great deal of profit.' }
        ]

        # 3. Blanks
        blanks_data = [
            { "text": "The cat jumped ___ the wall.", "blank": "over", "options": ["over", "under", "through", "between"] },
            { "text": "I have been living here ___ 2015.", "blank": "since", "options": ["for", "since", "from", "in"] },
            { "text": "She speaks English very ___.", "blank": "well", "options": ["good", "well", "better", "best"] },
            { "text": "If I ___ you, I would study harder.", "blank": "were", "options": ["was", "am", "were", "be"] },
            { "text": "They are looking forward to ___ you.", "blank": "seeing", "options": ["see", "saw", "seeing", "seen"] }
        ]

        # 4. Memory
        memory_data = [
            { "id": 1, "type": "A", "text": "Abundant" }, { "id": 1, "type": "B", "text": "Plentiful" },
            { "id": 2, "type": "A", "text": "Eager" }, { "id": 2, "type": "B", "text": "Keen / Enthusiastic" },
            { "id": 3, "type": "A", "text": "Diligent" }, { "id": 3, "type": "B", "text": "Hard-working" },
             { "id": 4, "type": "A", "text": "Obsolete" }, { "id": 4, "type": "B", "text": "Out of date" },
            { "id": 5, "type": "A", "text": "Vast" }, { "id": 5, "type": "B", "text": "Very large" },
            { "id": 6, "type": "A", "text": "To conceal" }, { "id": 6, "type": "B", "text": "To hide" }
        ]

        # Loading
        for q in quiz_data:
            Question.objects.get_or_create(category='QUIZ', content=q, is_static=True)
        
        for v in vocab_data:
            Question.objects.get_or_create(category='VOCAB', content=v, is_static=True)

        for b in blanks_data:
            Question.objects.get_or_create(category='BLANKS', content=b, is_static=True)

        for m in memory_data:
            Question.objects.get_or_create(category='MEMORY', content=m, is_static=True)

        self.stdout.write(self.style.SUCCESS('Successfully loaded static questions'))
