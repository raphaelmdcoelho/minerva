# Goal

The goal of this project is to assist in the generation of content for blog articles, through the creation of structured text content and images following the pattern of the prompt informed by the user and allowing the input of some parameters for the standardization of images and generated content.

# Structure

```
/myproject
    /app
        __init__.py
        /api
            __init__.py
            /v1
                __init__.py
                /resources
                    __init__.py
                    example.py
                /models
                    __init__.py
                    model.py
        /tests
            __init__.py
            test_config.py
            /api
                __init__.py
                /v1
                    __init__.py
                    test_example.py
        /utils
            __init__.py
            utility.py
    /instance
        config.py
    /migrations
    /scripts
        start_server.sh
    .env
    .flaskenv
    config.py
    requirements.txt
    run.py
```

* /app: Main application package.
    * /api: Contains the API blueprints, separated by version (e.g., v1).
        * /v1: Version 1 of the API.
            * /resources: Endpoints of the API.
            * /models: Database models (if using an ORM like SQLAlchemy).
    * /tests: Unit and integration tests.
    * /utils: Utility functions and classes.
* /instance: Configuration files that shouldn't be committed to version control (e.g., secrets).
* /migrations: Database migrations scripts (if using a migration tool like Flask-Migrate).
* /scripts: Utility scripts, like startup scripts.
* .env / .flaskenv: Environment variables for development.
* config.py: Configuration settings that can be committed to version control.
* requirements.txt: Project dependencies.
* run.py: Entry point to run the Flask application (linux).
* run-windows.py: Entry point to run the application through Windows.
* Dockerfile: Configuration file to create a container that hosts the application.

# How to run

## Locally (without container)

### Install python

```bash
python --version
```

or 

```bash
pytho3n --version
```

If Python is not installed, download and install it from the official `Python website`.

### Create a virtual Environment

Navigate to your project's root directory in the terminal or command prompt. Create a virtual environment using the venv module. Replace env with the name you wish to give to your virtual environment:

```bash
[python | python3] -m venv env
```

This command creates a directory called env in your project directory, containing a complete Python environment.

### Activate the Virtual Environment

On Windows, run:

```bash
env\Scripts\activate
```

On macOS and Linux, run:

```bash
source env/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

**Running through Flask**

```bash
flask run
```

**Running on Linux (WSL)**

```bash
gunicorn run:app
```

**Running on Windows**
```bash
waitress run-windows.py
```

**Checking**

Linux:

```bash
curl http://localhost:5000/api/v1/test
```

Windows:

Open the browser and go to the following URL: `http://localhost:5000/api/v1/test`

You should receive a response like:

```json
{
  "message": "Hello, World!"
}
```

### Deactivate the Virtual Environment

When you're done working on your project, you can deactivate the virtual environment to return to your global Python environment. Simply run:

```bash
deactivate
```
## Running through a container

```bash
docker build -t my-flask-app .
```

```bash
docker run -p 5000:5000 my-flask-app
```

## Testing

From the root project folder, execute the following command:

```bash
python -m unittest discover ./src/app/tests  
```

## Environment Variables and Secrets

`FLASK_APP`: Tells Flask which application it should run. This could be the name of the Python file that creates your Flask application instance.

`FLASK_RUN_HOST`: By default, the Flask development server listens on `localhost`. This is fine when you're running the server directly on your host machine because you can access your Flask application by visiting `http://localhost:5000` in your web browser. However, when running inside a Docker container, if Flask listens only on `localhost`, the application won't be accessible from outside the container because `localhost` inside the container is isolated from `localhost` on your host machine. Setting it to be `0.0.0.0` tells Flask to listen on all network interfaces inside the container. This setup allows incoming connections not just from within the container, but also from outside the container, including from your host machine.

`OPENAI_API_KEY`: OpenAI api secret key value.

## General Information


## Notes

```bash
pip freeze > requirements.txt
```

```bash
pip list
```

* For production deployments, it's recommended to use a production-ready WSGI (Web Server Gateway Interface) server. Some of the most popular WSGI servers for deploying Flask applications include Gunicorn, uWSGI, and Phusion Passenger.

Why Not Use Flask's Built-in Server in Production?
Performance: Flask's built-in server is not optimized for speed and can handle only a limited amount of traffic. Production WSGI servers, on the other hand, are designed to efficiently manage multiple requests simultaneously.
Security: The development server does not include security features necessary to protect your application against attacks.
Reliability: Production servers offer better error handling and logging capabilities, which are essential for diagnosing and fixing issues in a production environment.

Behind a Reverse Proxy: In a production environment, Gunicorn should be placed behind a reverse proxy server like Nginx or Apache. The reverse proxy handles HTTP requests from clients and forwards them to Gunicorn, adding an additional layer of security and allowing you to use features like SSL/TLS encryption.

Gunicorn cannot run natively on Windows environments.