from django.http import JsonResponse
from .models import Question, Rule

def process_question(request, question_id):
    response = request.GET.get('response')
    
    if not response:
        return JsonResponse({'error': 'Response is required'}, status=400)
    
    try:
        question = Question.objects.get(id=question_id)
        rules = Rule.objects.filter(question=question)

        for rule in rules:
            if eval(rule.condition):
                if rule.next_question:
                    return JsonResponse({'next_question_id': rule.next_question.id})
                if rule.message:
                    return JsonResponse({'message': rule.message})
        return JsonResponse({'message': 'No valid rule found'})
    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)
