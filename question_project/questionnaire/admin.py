from django.contrib import admin
from .models import Question, Answer, Rule

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'text')
    search_fields = ('text',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'response', 'user', 'created_at')
    list_filter = ('question', 'created_at')
    search_fields = ('response', 'question__text')
    readonly_fields = ('created_at',)  # Make 'created_at' read-only in the detail view

    # define the fields to be displayed in the detail view
    fields = ('question', 'response', 'user', 'created_at')


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'condition', 'next_question', 'message')
    search_fields = ('question__text', 'condition', 'message')
