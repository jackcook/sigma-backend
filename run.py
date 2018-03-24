from flask import Flask
from app import configure_app

# Create and configure the Flask application
application = Flask(__name__)
configure_app(application)

if __name__ == "__main__":
    # Run the Flask app if this is called from the command line
    application.run()
