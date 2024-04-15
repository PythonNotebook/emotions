from api import *
from api import __import__


if __name__ == '__main__':
    app.register_blueprint(rest)
    app.run(debug=True)
