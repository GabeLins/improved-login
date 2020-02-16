from LoginSystem import app, db
import os

if __name__ == '__main__':
    if ( not os.path.exists('./LoginSystem/data') ):
        os.mkdir('./LoginSystem/data')
    
    db.create_all(app=app)
    app.run('0.0.0.0', 4444, debug=True)
