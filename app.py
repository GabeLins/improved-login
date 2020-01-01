from os import environ
from LoginSystem import app

if __name__ == '__main__':
    app.run('localhost', 4444, debug=True)