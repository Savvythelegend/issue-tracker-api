# This file is used to run the Flask application.
# It imports the create_app function from the app package and runs the application.
# The debug mode is enabled for development purposes.
# To run the application, use the command: python run.py
# Make sure to have the necessary environment variables set up before running the application.
# For production, consider using a WSGI server like Gunicorn or uWSGI instead of the built-in Flask server.
# Ensure that the app package is structured correctly with an __init__.py file.
# The create_app function should handle the application configuration and initialization.
# This setup allows for easy testing and deployment of the Flask application.

from app import create_app

app = create_app()
if __name__ == "__main__":
    app.run()
