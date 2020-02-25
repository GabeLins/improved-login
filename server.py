from setup import setup
import os

path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(path, 'LoginSystem/data')
key_path = os.path.join(path, 'server.key')


if __name__ == '__main__':
    args = setup()

    # Import modules
    from LoginSystem.security import generate_ssl
    from LoginSystem import app, db, settings

    if ( not os.path.exists(db_path) ):
        os.mkdir(db_path)

    if ( args.ssl and not os.path.exists(key_path) ):
        generate_ssl()

    print(f' * Server SECRET_KEY: {app.config["SECRET_KEY"]}')
    
    db.create_all(app=app)
    app.run(
        settings['server_addr'], settings['server_port'], 
        debug=args.debug,
        ssl_context=args.ssl
    )
