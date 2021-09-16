from app import create_app
from flask_script import Manager
from flask import Flask

app=create_app()

manager=Manager(app)


@manager.command
def run():
    app.debug = True # test debug
    app.run(port=5000, host='0.0.0.0')


if __name__ == "__main__":
    manager.run()