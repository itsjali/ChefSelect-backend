import jwt
import re

from datetime import datetime, timedelta
from typing import Tuple, Dict
from flask import jsonify
from flask_bcrypt import check_password_hash

from app.models import db, User
from app import bcrypt

# Regex for validating an Email
EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class CreateNewUser:
    def __init__(self, name: str, email: str, password: str):
        self.name = name
        self.email = email
        self.password = password
    
    def run(self):
        if not self.email or not self.password:
            return jsonify({"error": "Email or password are required"}), 400
        
        if not re.match(EMAIL_REGEX, self.email):
            return jsonify({"error": "Invalid email format"}), 400
        
        if len(self.password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400
        
        existing_email = User.query.filter_by(email=self.email).first()
        if existing_email:
            return jsonify({"error": "User already exists"}), 400
        
        hashed_password = bcrypt.generate_password_hash(self.password).decode("utf-8")

        # Create new user
        new_user = User(email=self.email, password=hashed_password, name=self.name)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully", "email": self.email}), 201


class AuthenticateUser:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def validate(self, email: str, password: str) -> Tuple[Dict[str, str], int]:
        if not email or not password:
            return jsonify({"error": "Email or password are required"}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid email or password"}), 401
        
        return {"user_id": user.id}, 200
    
    def generate_tokens(self, user_id: int) -> Tuple[Dict[str, str], int]:
        access_token = jwt.encode({
            "user_id": user_id,
            "exp": datetime.now() + timedelta(hours=1)
        }, self.secret_key, algorithm="HS256")

        refresh_token = jwt.encode({
            "user_id": user_id,
            "exp": datetime.now() + timedelta(days=7)
        }, self.secret_key, algorithm="HS256")

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }), 200

    def refresh_access_token(self, refresh_token: str) -> Tuple[Dict[str, str], int]:
        try:
            decoded_refresh_token = jwt.decode(refresh_token, self.secret_key, algorithms=["HS256"])
        
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Refresh token has expired"}), 401
        
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid refresh token"}), 401

        # Generate a new access token
        new_access_token = jwt.encode({
            "user_id": decoded_refresh_token["user_id"],
            "exp": datetime.now() + timedelta(hours=1)
        }, self.secret_key, algorithm="HS256")

        return jsonify({"access_token": new_access_token}), 200