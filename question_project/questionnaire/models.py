from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)
    options = models.JSONField()  # Storing options as JSON

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.JSONField()  # Store response as JSON

    def __str__(self):
        return f"Answer to {self.question.text}"

class Rule(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    condition = models.TextField()
    next_question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.SET_NULL, related_name='next_question')
    message = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Rule for {self.question.text}"
