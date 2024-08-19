def custom_condition_example(response, previous_responses):
    """
    Example condition that checks if the current response is 'Yes'
    and if the response to question 2 was also 'Yes'.
    """
    return response == 'Yes' and previous_responses.get('question_2') == 'Yes'


def custom_income_condition_cali(response, previous_responses):
    """
    Custom condition that checks if the current response is 'Yes',
    the user has a previous income response of either '$50,000 - $100,000' or '$100,000+',
    and the response to question_2 (do you live in California) is 'Yes'.
    """
    question_1_response = previous_responses.get('question_1')
    question_2_response = previous_responses.get('question_2')

    print(f"Response: {response}")
    print(f"Question 1 Response: {question_1_response}")
    print(f"Question 2 Response: {question_2_response}")

    return (
        response == 'Yes' and
        question_1_response in ['$50,000 - $100,000', '$100,000+'] and
        question_2_response == 'Yes'
    )



