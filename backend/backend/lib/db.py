from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app, db):
    db.init_app(app)
    return db
