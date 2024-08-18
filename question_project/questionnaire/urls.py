from django.urls import path
from . import views

urlpatterns = [
    path('process_question/<int:question_id>/', views.process_question, name='process_question'),
]