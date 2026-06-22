from flask_restful import Resource
from flask import Flask, request, jsonify
from models.Trades import Trades
import requests
from lib.db import db
from datetime import datetime
from sqlalchemy import asc, desc

class AddTrade(Resource):
    def post(self):
        requestedData = request.json
        # print(requestedData)
        userId = requestedData['userId']
        symbol = requestedData['symbol']
        amount = requestedData['amount']
        profitLimit = requestedData['profitLimit']
        stopLoss = requestedData['stopLoss']
        createdAt = requestedData['time'] if requestedData['time'] else datetime.utcnow()
        print(requestedData)

        newTrade = Trades(userId=userId, symbol=symbol, amount=amount, position=0, profitLimit = profitLimit, stopLoss = stopLoss, status=0, createdAt = datetime.utcnow())

        # db.session.add(newTrade)
        # db.session.commit()

        # return jsonify({'message': 'Trade Added Successfully', 'status': 200})
        try:
            db.session.add(newTrade)
            db.session.commit()  
        except Exception as e:
            db.session.rollback() 
            return jsonify({'message': str(e), 'status': 500})
        finally:
            db.session.close()

class RecentTrades(Resource):
    def get(self):
        currentUserId = request.args.get("userId")
        recentTradesQuery = Trades.query.with_entities(Trades.id, Trades.symbol, Trades.position, Trades.amount, Trades.status, Trades.createdAt, Trades.userId).filter_by(userId=currentUserId).order_by(desc(Trades.id)).limit(20).all()

        tradeList = []
        for trade in recentTradesQuery:
            tradeList.append(trade._asdict())
        
        return jsonify({'message': 'Trade Added Successfully', 'data': tradeList, 'status': 200})


class ExecuteTrade(Resource):
    def get(self):
        tradesQuery = Trades.query.with_entities(Trades.id, Trades.symbol, Trades.position, Trades.amount, Trades.status, Trades.createdAt, Trades.userId).filter_by(status=0).order_by(asc(Trades.id)).first()
