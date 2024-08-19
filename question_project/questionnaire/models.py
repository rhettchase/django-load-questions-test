from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    CHOICE = 'choice'
    TEXT = 'text'
    NUMBER = 'number'
    DATE = 'date'
    BOOLEAN = 'boolean'

    DATA_TYPE_CHOICES = [
        (CHOICE, 'Choice'),
        (TEXT, 'Text'),
        (NUMBER, 'Number'),
        (DATE, 'Date'),
        (BOOLEAN, 'Boolean'),
    ]

    text = models.CharField(max_length=255)
    options = models.JSONField(blank=True, null=True)  # Store options as JSON
    data_type = models.CharField(max_length=50, choices=DATA_TYPE_CHOICES)  # Restrict to specific choices

    def __str__(self):
        return self.text

class Rule(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    condition = models.TextField() # Store the condition as a text expression
    next_question = models.ForeignKey(Question, related_name='next_question', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Rule for {self.question.text}"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the answer to a specific user
    response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question.text}: {self.response}"
