# Setup and Run Instructions for FastAPI Image Renamer

## Prerequisites
- Python 3.9+ installed
- Git installed
- Virtual environment (recommended)

## Steps

1. Clone the Repository:
   git clone https://github.com/TejasMane-developer/fastapi-image-renamer.git

2. Navigate into the project directory:
   cd fastapi-image-renamer

3. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate

4. Install dependencies:
   pip install -r requirements.txt

5. Create a `.env` file in the project root with the following variables:
   APP_HOST=127.0.0.1
   APP_PORT=3000

6. Run the server using dotenv:
   dotenv run -- uvicorn main:app --host $APP_HOST --port $APP_PORT --reload

7. Access the application in your browser:
   http://127.0.0.1:3000

8. API Documentation available at:
   http://127.0.0.1:3000/docs