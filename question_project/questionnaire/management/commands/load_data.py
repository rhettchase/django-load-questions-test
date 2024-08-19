import json
from django.core.management.base import BaseCommand
from questionnaire.models import Question, Rule

class Command(BaseCommand):
    help = 'Load questions and rules from JSON files'

    def handle(self, *args, **kwargs):
        self.load_questions()
        self.load_rules()

    def load_questions(self):
        with open('data/questions.json') as f:
            questions = json.load(f)
            for question in questions:
                Question.objects.update_or_create(
                    id=question['id'],
                    defaults={
                        'text': question['text'],
                        'options': question['options'],
                        'data_type': question['data_type'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded questions from JSON'))

    def load_rules(self):
        with open('data/rules.json') as f:
            rules = json.load(f)
            for rule in rules:
                question = Question.objects.get(id=rule['question_id'])
                next_question = Question.objects.get(id=rule['next_question_id']) if rule['next_question_id'] else None

                Rule.objects.update_or_create(
                    id=rule['id'],
                    defaults={
                        'question': question,
                        'condition': rule['condition'],
                        'next_question': next_question,
                        'message': rule['message'],
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded rules from JSON'))
