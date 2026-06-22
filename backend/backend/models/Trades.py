from flask_sqlalchemy import SQLAlchemy
from lib.db import db

class Trades(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    symbol = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    position = db.Column(db.Integer, nullable=False)
    stopLoss = db.Column(db.Integer, nullable=False)
    profitLimit = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    createdAt = db.Column(db.String(100))

    # def __reper__():
    #     return f"Video(name={name}, views={views}, likes={likes})"

    def __init__(self, userId='', symbol='', amount=0, stopLoss=0, profitLimit=0, position=0, status=0, createdAt=None):
        self.userId = userId
        self.symbol = symbol
        self.status = status
        self.amount = amount
        self.stopLoss = stopLoss
        self.profitLimit = profitLimit
        self.position = position
        self.createdAt = createdAt
# db.create_all()