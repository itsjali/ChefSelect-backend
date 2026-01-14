import jwt
import os

from flask import current_app, jsonify, request

from app.models import User


APP_ENV = os.getenv("APP_ENV")
AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
BYPASS_TOKEN_AUTH = os.getenv("BYPASS_TOKEN_AUTH")


def token_required(view):
    def wrapper(*args, **kwargs):
        if APP_ENV != "production" and BYPASS_TOKEN_AUTH == "true":
            current_app.logger.info("Bypassing Token Authentication")
            return view(*args, **kwargs)
        
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        
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