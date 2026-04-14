from flask_app import app
from flask_app.controllers.users import *
from flask_app.controllers.tasks import *


if __name__ == '__main__':
    app.run(debug=True)