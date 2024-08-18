from django.db import models

class Question(models.Model):
    text = models.CharField(max_length=255)
    options = models.JSONField(blank=True, null=True)  # To handle JSON options
    data_type = models.CharField(max_length=50)

    def __str__(self):
        return self.text

class Rule(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    condition = models.TextField()
    next_question = models.ForeignKey(Question, related_name='next_question', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Rule for {self.question.text}"
