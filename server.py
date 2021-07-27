from flask_app import app

from flask_app.controllers import login, dashboard # write down name of second controller

if __name__ == ('__main__'):
    app.run(debug=True)


# pipenv shell