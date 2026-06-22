from flask_restful import Resource
from flask import Flask, request, jsonify
from models.User import User
import requests
from lib.db import db
from datetime import datetime
import json 
# db.create_all()

class Login(Resource):
    def post(self):
        email = request.json['email']
        password = request.json['password']
        if (email is None or email == '') and (password is None or password == ''):
            return jsonify({'message': 'Bad Request', 'status': 400})
        
        user = User.query.with_entities(User.id, User.email, User.username).filter_by(email=email).filter_by(password=password).first()
        # print(json.dumps(user))
        # print(user)

        if not user:
            return jsonify({'message': 'Invalid credentials', 'status': 401})
        else:
            # print(user.to_dict())
            # return jsonify({'message': 'Login Successfull', 'data': user, 'status': 200})
            user_dict = {
            'id': user.id,
            'email': user.email,
            'username': user.username
        }

        return jsonify({'message': 'Login Successful', 'data': user_dict, 'status': 200})
    
class SignUp(Resource):
    def post(self):
        data = request.json
        # username = data['username']
        password = data['password']
        email = data['email']

        user = User(password=password, email=email, createdAt = datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        userId = user.id
        userData = User.query.with_entities(User.id, User.email, User.username).filter_by(id=userId).first()

        return jsonify({'message': 'Signup Successfull', 'data': userData, 'status': 200})
