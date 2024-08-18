from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Question, Rule
import json

@csrf_exempt
@require_POST
def process_question(request, question_id):
    try:
        body = json.loads(request.body)
        response = body.get('response')
        
        if not response:
            return JsonResponse({'error': 'Response is required'}, status=400)
        
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
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
