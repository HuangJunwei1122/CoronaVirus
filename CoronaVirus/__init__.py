from flask import Flask

app = Flask('CoronaVirus')
app.config.from_pyfile('settings.py')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

from CoronaVirus import views

if __name__ == '__main__':
    app.run()
