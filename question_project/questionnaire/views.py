from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Question, Rule
import json
import logging
from . import conditions  # Import your custom conditions module

logger = logging.getLogger(__name__)

@csrf_exempt
@require_POST
def process_question(request, question_id):
    try:
        body = json.loads(request.body)
        response = body.get('response')
        previous_responses = body.get('previous_responses', {})
        user_id = body.get('user_id')

        if not response:
            return JsonResponse({'error': 'Response is required'}, status=400)

        question = Question.objects.get(id=question_id)
        rules = Rule.objects.filter(question=question)

        # Create a context with the custom functions
        eval_context = {
            "response": response,
            "previous_responses": previous_responses,
            "custom_income_condition_cali": conditions.custom_income_condition_cali,
        }

        for rule in rules:
            try:
                condition_expression = rule.condition
                logger.info(f"Evaluating rule: {condition_expression} with context: {eval_context}")
                result = eval(condition_expression, {}, eval_context)
                logger.info(f"Condition: {condition_expression} evaluated to: {result}")
                if result:
                    if rule.next_question:
                        return JsonResponse({'next_question_id': rule.next_question.id})
                    if rule.message:
                        return JsonResponse({'message': rule.message})
            except Exception as e:
                logger.error(f"Error evaluating rule: {condition_expression}, error: {str(e)}")
        
        # Log context if no rule matches
        logger.info(f"No valid rule found with context: {eval_context}")
        return JsonResponse({'message': 'No valid rule found'})

    except Question.DoesNotExist:
        return JsonResponse({'error': 'Question not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

