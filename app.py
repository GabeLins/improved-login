from LoginSystem.security import *
from LoginSystem import app, db
import os

path = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(path, 'LoginSystem/data')
configs_path = os.path.join(path, 'app.cfg')
cert_path = os.path.join(path, 'server.key')

def setup ():
    if ( not os.path.exists(database_path) ):
        os.mkdir(database_path)

    if ( not os.path.exists(configs_path) ):
        generate_secret_key(configs_path)

    if ( not os.path.exists(cert_path) ):
        generate_certificate()

    return 0


if __name__ == '__main__':
    setup()
    
    app.config.from_pyfile(configs_path)
    db.create_all(app=app)
    ctx = ('server.crt', 'server.key')

    app.run('0.0.0.0', 443, ssl_context=ctx)
