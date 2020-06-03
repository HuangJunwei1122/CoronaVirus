from flask import Flask
# from flask_wtf.csrf import CSRFProtect


app = Flask('CoronaVirus')
app.config.from_pyfile('settings.py')
# csrf = CSRFProtect(app)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

from CoronaVirus import views

