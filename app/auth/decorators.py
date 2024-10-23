import jwt
import os

from flask import jsonify, request

from app.models import User

AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY") 


def token_required(view):
    def wrapper(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1] # Extract token
        
        if not token:
            return jsonify({"error": "Token is not present"}), 401
        
        try:
            data = jwt.decode(token, AUTH_SECRET_KEY, algorithms=["HS256"])
            user = User.query.filter_by(id=data["user_id"]).first()

            if not user:
                return jsonify({"error": "User not found"}), 401
            
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401

        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401 
        
        # If token is valid, pass the user object to the view function
        return view(*args, **kwargs)

    return wrapper 