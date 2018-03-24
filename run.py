from flask import Flask
import os, sys

from app import configure_app

application = Flask(__name__)
configure_app(application)

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=5001, debug=True)
