# Movie collection

## Introduction

Web application which allows people to create collections of movies they like. 
A third party movie api is used to get list of movies, from that user in this 
application can create their own movie collections. Crud operations implemented for 
the collections. Also, there is a monitoring system to find number of request comes to the
application.

## Getting Started

### Prerequisites
- Python (version 3.11.0)
- Django (version 5.0.1)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Aswanym/onefin-assignment.git
   
2. Create virtual environment
   ```bash
      virtualenv venv
   
3. activate virtualenv (windows)
   ```bash
      venv/Scripts/activate
   
4. Install dependencies
   ```bash
      pip install -r requirements.txt
      
   
5. Configuration
- Create a .env file in the project root. 
- Add the following environment variables to the .env file:

   ```bash
  # Django Secret Key
  SECRET_KEY=your_secret_key
  DEBUG=your_debug
  
  # Movie api credentials
  MOVIE_API_URL=movie_api_url
  API_CLIENT=api_username
  API_CLIENT_SECRET=api_password
  
- Replace the placeholder values with your actual values.

6. Database Migration
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   
7. Running the Server - Start the development server:
   ```bash
   python manage.py runserver

8. Visit http://localhost:8000/ in your browser to view your project.


##### References

Python Requests' Retry Logic - https://www.zenrows.com/blog/python-requests-retry#what-to-know, https://stackoverflow.com/questions/23267409/how-to-implement-retry-mechanism-into-python-requests-library

JWT Authentication in DRF with Simple-JWT - https://osirusdjodji.medium.com/jwt-authentication-in-django-rest-framework-with-simple-jwt-a-comprehensive-guide-f2ba860f1365

Use JWT Authentication for User login in DRF - https://www.linkedin.com/pulse/use-jwt-authentication-user-login-django-rest-framework-jagrat-patel/

JWT token with postman - https://learning.postman.com/docs/sending-requests/authorization/authorization-types/#bearer-token

cache - https://medium.com/@harshgolu82/utilizing-djangos-cache-incr-method-79daf794db82#:~:text=After%20a%20bit%20of%20research,additional%20variables%20and%20complex%20logic.
