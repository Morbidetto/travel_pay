This Django application can modify user balance, view their data and import users data from csv file.
Operations can be performed using REST API.

#### Stack
* Python 3.8
* Django 2.3
* djangorestframework 3.11
* MySQL 8

### Start
Application is dockerized but can also be run locally. Firstly copy env_example into .env file and modify variables to your liking.
* To run inside docker run `docker-compose up -d`
* To run locally create local environment and install libraries from requirements.txt. Remember to configure DATABASE_URL env variable. 
* To run tests run `pytest`
* Endpoints documentation is available on /docs endpoint.

### To do
* App would benefit from frontend application which would handle REST communication. 
* Account model is seperated from Django User model and there's no authentication and authorisation. 
* Everyone can access all endpoints and they should be restricted to special user type.
