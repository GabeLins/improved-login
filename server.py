from setup import setup
import os

# Default paths
path = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(path, 'LoginSystem/data')
key_path = os.path.join(path, 'server.key')

# Main script
if __name__ == '__main__':
    # Get command-line arguments
    args = setup()

    # Import application modules
    from LoginSystem.security import generate_ssl
    from LoginSystem import app, db, settings

    # Check if database file exist
    if ( not os.path.exists(db_path) ):
        os.mkdir(db_path)

    # Generate a SSL certificate
    if ( args.ssl and not os.path.exists(key_path) ):
        generate_ssl()

    # Print your secret key
    print(f' * Server SECRET_KEY: {app.config["SECRET_KEY"]}')
    
    # Create the database and execute the app
    db.create_all(app=app)
    app.run(
        settings['server_addr'], settings['server_port'], 
        debug=args.debug,
        ssl_context=args.ssl
    )
