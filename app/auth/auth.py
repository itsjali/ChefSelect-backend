import os 
import requests

from cachecontrol import CacheControl
from flask import Blueprint, abort, jsonify, redirect, request, session
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from google.auth.transport import requests as google_requests

from app.auth.services import AuthenticateUser, CreateNewUser
from app.models import db, User

auth_bp = Blueprint("auth", __name__)


google_callback_url = os.getenv("GOOGLE_CALLBACK_URL")
google_client_id = os.getenv("GOOGLE_CLIENT_ID")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
google_project_id = os.getenv("GOOGLE_BACKEND_PROJECT_ID")
google_user_profile_api = os.getenv("GOOGLE_USER_PROFILE_API")
google_user_email_api = os.getenv("GOOGLE_USER_EMAIL_API")

def create_client_secrets_file():
    secrets_file = {
        "web": {
            "client_id": google_client_id,
            "project_id": google_project_id,
            "auth_uri":"https://accounts.google.com/o/oauth2/auth",
            "token_uri":"https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
            "client_secret":google_client_secret,
            "redirect_uris":[google_callback_url],
        }
    }
    return secrets_file
    
flow = Flow.from_client_config(
    client_config=create_client_secrets_file(),
    scopes=[google_user_profile_api, google_user_email_api, "openid"],
    redirect_uri=google_callback_url,
)


@auth_bp.route("/google-login")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auth_bp.route("/callback")
def callback():
    # Exchange auth code for a token
    flow.fetch_token(authorization_response=request.url)
    
    # Retrieve credentials from the OAuth flow
    credentials = flow.credentials

    # Create session
    request_session = requests.Session()
    cached_session = CacheControl(request_session)
    token_request = google_requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials.id_token,
        request=token_request,
        audience=google_client_id,
    )
    
    email = id_info.get("email")
    session["email"] = email

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(email=email)
        db.session.add(user)
        db.session.commit()

    auth_service = AuthenticateUser(secret_key=os.getenv("AUTH_SECRET_KEY"))
    token_response, status_code = auth_service.generate_tokens(user.id)
    
    if status_code != 200:
        return abort(status_code)

    access_token = token_response.json.get("access_token")
    refresh_token = token_response.json.get("refresh_token")

    frontend_url = os.getenv("REACT_FRONTEND_URL")
    return redirect(f"{frontend_url}/google-redirect?access_token={access_token}&refresh_token={refresh_token}")


@auth_bp.route("/sign-up", methods=["POST"])
def sign_up():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    service = CreateNewUser(name, email, password)
    return service.run()


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    auth_service = AuthenticateUser(secret_key=os.getenv("AUTH_SECRET_KEY"))
    result, status_code = auth_service.validate(email=email, password=password)
    if status_code != 200:
        return result, status_code

    return auth_service.generate_tokens(result["user_id"])


@auth_bp.route("/refresh-token", methods=["POST"])
def refresh_token():
    data = request.get_json()
    refresh_token = data.get("refresh_token")
    
    auth_service = AuthenticateUser(secret_key=os.getenv("AUTH_SECRET_KEY"))
    return auth_service.refresh_access_token(refresh_token=refresh_token)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Successfully logged out"}), 200