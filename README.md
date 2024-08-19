# Django Questionnaire Backend

This Django project provides a backend for managing questionnaires with dynamic rules, where questions, options, and rule logic are loaded and updated using JSON files.

## Features

- Load questions and rules from JSON files.
- The questions JSON file contains all the questions, options, and their data types.
- The rules JSON file contains the rules/conditions that dictate what the next question will be based on user responses.
- Process user responses and navigate through the questionnaire based on predefined rules.
- Admin interface for managing questions and rules.
- Easily update the database by modifying JSON files and running the update command.

## Getting Started

1. Clone repository

2. Setup virtual environment

3. Install dependencies `pip install -r requirements.txt`

4. Setup the database

  - If you're using PostgreSQL, update the DATABASES setting in question_project/settings.py with your PostgreSQL credentials. By default, this project uses SQLite.

```python
# Example PostgreSQL settings in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_database_name',
        'USER': 'your_database_user',
        'PASSWORD': 'your_database_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

5. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser `python manage.py createsuperuser`

7. Load questions and rules from the JSON Files

  - Place your questions.json and rules.json files in the data/ directory (or update the path in the command below if they're stored elsewhere). Then, run the following command to load the questions and rules into the database:

```bash
python manage.py load_data
```

8. Run the Development server: `python manage.py runserver`

  - The server will start running at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

9. Access the Admin Interface

  - Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) in your web browser and log in with the superuser account you created earlier. Here, you can manage questions and rules.

10. Test the questionnaire logic by visiting the below route. Send a POST request with the tool of your choice (e.g. Thunder Client or curl)

POST route: `http://127.0.0.1:8000/questionnaire/process_question/<question_id>/`

### Example Scenario:

1. Start by answering the first question (income).
2. Depending on the income, the next question might be about living in California.
3. Based on both the response to the income question and the response to whether they live in California, a specific question or message might be shown.

**Step 1:** Respond to first question (income)

```bash
curl -X POST http://127.0.0.1:8000/questionnaire/process_question/1/ \
-H "Content-Type: application/json" \
-d '{"response": "$50,000 - $100,000", "user_id": 1}'

```

expected response

```json
{
    "next_question_id": 2
}
```

**Step 2:** Respond to second question (California)

```bash
curl -X POST http://127.0.0.1:8000/questionnaire/process_question/2/ \
-H "Content-Type: application/json" \
-d '{"response": "Yes", "user_id": 1}'
```

expected response:

```json
{
    "next_question_id": 4
}
```

**Step 3:** This response should consider both the response to the third question (premium program) and the previous responses to the income and California questions, using the custom logic defined in conditions.py.

```bash
curl -X POST http://127.0.0.1:8000/questionnaire/process_question/3/ \
-H "Content-Type: application/json" \
-d '{
    "response": "Yes",
    "user_id": 1,
    "previous_responses": {
        "question_1": "$50,000 - $100,000",
        "question_2": "Yes"
    }
}'
```

expected response

```json
{
  "next_question_id": 5
}
```

## Updating the Database

1. Modify JSON Files
Update questions.json and/or rules.json with the new or modified questions and rules.
2. Run the Update Command

Run the same command you used for the initial data seeding to update the database: `python manage.py load_data`

  - This command will update existing records and add any new ones based on the contents of the JSON files.

## Additional Notes

- For production deployment, consider using a more robust setup with a WSGI server like Gunicorn, and a web server like Nginx.
- `process_question` view [views.py](./question_project/questionnaire/views.py) accepts POST requests with the response data included in the request body.

If you’re sending the data to a frontend application, you can use the following approach:

1. Frontend Tracks Responses:

  - As the user answers each question, the frontend application keeps track of their responses in a local state (e.g., using JavaScript, React state, or any other frontend framework).

2. Constructing the Payload:

  - When the user submits a response to a question, the frontend constructs the payload. This payload includes the current response as well as any previous responses that might be needed for evaluating rules.

```javascript
const previousResponses = {
    question_1: "Under $20,000",
    question_2: "Yes"
};

const payload = {
    response: "Yes",  // Current response to question 3
    previous_responses: previousResponses
};
```

3. Sending the payload to the backend:

  - The frontend sends this payload to the backend via a POST request. The Django backend then processes this payload, evaluates the conditions, and returns the next question or message.

Example POST Request:

```javascript
fetch('http://127.0.0.1:8000/questionnaire/process_question/3/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
})
.then(response => response.json())
.then(data => {
    console.log('Next step:', data);
    // Handle the next step, e.g., displaying the next question
})
.catch(error => console.error('Error:', error));

```

### CSRF Considerations

Note that I included `@csrf_exempt` in the view decorator for simplicity. However, for production environments, it’s crucial to handle CSRF tokens properly in Django for security reasons. If you’re working with a frontend, you should ensure that the CSRF token is included in the request headers.
