from django.contrib import admin
from .models import Question, Answer, Rule

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    search_fields = ('text',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'response')
    search_fields = ('question__text',)

@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'condition', 'next_question', 'message')
    search_fields = ('question__text', 'condition', 'message')
