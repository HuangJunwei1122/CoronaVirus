import os

from CoronaVirus import app


SECRET_KEY = os.getenv('SECRET_KEY', "hello, I'm a secret key")
