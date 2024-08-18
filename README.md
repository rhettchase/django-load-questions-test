# Django Questionnaire Backend

This Django project provides a backend for managing questionnaires with dynamic rules, where questions, options, and rule logic are loaded from an Excel file.

## Features

- Load questions and rules from an Excel file.
- The Question tab contains all questions
- The rules tab contains the rules/conditions that will dictate what the next question will be.
- Process user responses and navigate through the questionnaire based on predefined rules.
- Admin interface for managing questions and rules.

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

7. Load questions and rules from the Excel file. This repository contains a starter Excel file with the format

  - Place your questions_and_rules.xlsx file in the data/ directory (or update the path in the command below if it's stored elsewhere). Then, run the following command to load the questions and rules into the database:

```bash
python manage.py load_questions data/questions_and_rules.xlsx
```

8. Run the Development server: `python manage.py runserver`

  - The server will start running at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

9. Access the Admin Interface

  - Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) in your web browser and log in with the superuser account you created earlier. Here, you can manage questions and rules.

10. Test the questionnaire logic by visiting the below route. Send a POST request with the tool of your choice (e.g. Thunder Client or curl)

POST route: `http://127.0.0.1:8000/questionnaire/process_question/<question_id>/`

## Additional Notes

- For production deployment, consider using a more robust setup with a WSGI server like Gunicorn, and a web server like Nginx.
- `process_question` view [views.py](./question_project/questionnaire/views.py) accepts POST requests with the response data included in the request body.

If you’re sending the data to a frontend application, you can use the following approach:

```javascript
fetch('http://127.0.0.1:8000/questionnaire/process_question/1/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({response: 'Yes'}),
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

### CSRF Considerations

Note that I included `@csrf_exempt` in the view decorator for simplicity. However, for production environments, it’s crucial to handle CSRF tokens properly in Django for security reasons. If you’re working with a frontend, you should ensure that the CSRF token is included in the request headers.
