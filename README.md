# CSV User Data Processor API

A Django REST Framework API that processes user data from CSV files, validates the data, and stores valid records in a database.

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework 3.12+
- PostgreSQL 12+

## Installation

1. Extract the provided ZIP file to your desired location / Clone the repository:

2. Create a virtual environment and activate it:
python -m venv env
.\env\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt

4. Setup the database:
Update the database credentials in .env file

5. Apply migrations:
python manage.py makemigrations
python manage.py migrate

6. Run the development server:
python manage.py runserver

The API will be available at http://localhost:8000

## API Endpoints

### Upload CSV

- URL: `/api/upload-csv/`
- Method: POST
- Content-Type: multipart/form-data
- Parameter: file (CSV file)

#### Response Format

```json
{
"successful_records": 2,
"rejected_records": 3,
"errors": [
 {
   "row": 3,
   "data": {"name": "Invalid User", "email": "invalid-email", "age": 35},
   "errors": {"email": ["Enter a valid email address."]}
 },
 {
   "row": 4,
   "data": {"name": "Old Person", "email": "old@example.com", "age": 150},
   "errors": {"age": ["Age must be an integer between 0 and 120"]}
 },
 {
   "row": 5,
   "data": {"name": "", "email": "empty@example.com", "age": 40},
   "errors": {"name": ["Name cannot be empty"]}
 }
]
}
