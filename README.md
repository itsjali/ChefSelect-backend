# ChefSelect-Backend

ChefSelect is a POC cookbook Flask-React application.

This small project is intended to build my knowledge on:
- Flask API development
- Docker-based local development
- Deploying to GCP + AWS RDS as the database
- Google SSO (OAuth) integration

_By all means, this is not a "production-ready" product._

## Installation 
```
git clone https://github.com/itsjali/chefselect-backend.git

docker compose build
```

## Start Backend
```
docker compose up

# Accessing the container:
docker compose exec web bash

# Manage using Flask inside the container:
flask shell
```

## Running Tests
```
# Access the docker container and run: 
python -m pytest

# or run a specific test
python -m pytest -k $TEST_NAME
```

## Testing the API
When testing the whole application, the Frontend and Backend servers need to be running, and you will need to register/login via Google SSO. Users who are authenticated and authorized can interact with the endpoints. 

However, the endpoints can still be tested without needing the Frontend. As soon as the Docker container starts up, a dev user is created (if not already created) from the `seed_dev_user` function. The endpoints are protected and requires the user to have a valid auth token. We can either replicate the token authentication to simulate the process more realistically or simply bypass it. 

### Token Authentication
Below is an example of how to create a token for the dev user and calling the `create-recipe` endpoint. The credentials for the dev user are saved in the `.env` file in the root directory. If the request is successful, this should create a recipe and saved in the DB. We can verify this by either accessing the DB (credentials are saved in the `.env` file) or accessing the Docker container and use Flask ORM  to make queries.
```
# Firstly, create a token from your terminal
TOKEN=$(
  curl -s -X POST http://127.0.0.1:5000/login \
    -H "Content-Type: application/json" \
    -d '{"email":"dev-backend-user@example.com","password":"dev-backend-password"}' \
  | jq -r .access_token
)

# Verify the token has been created
echo "$TOKEN"

# 
curl -i -X POST http://127.0.0.1:5000/create-recipe \
-H "Content-Type: application/json" \
-H "Authorization: Bearer $TOKEN" \
-d '{
    "title": "Chicken & Rice",
    "description": "Quick, easy and slightly boring dinner",
    "ingredients": [{"name": "chicken", "unit": "200g"}, {"name": "rice", "unit": "150g"}],
    "instructions": ["Cook chicken", "Cook rice"]
  }'
```

### The Lazy Way
If you want to bypass the token authentication, set `BYPASS_TOKEN_AUTH` in the `.env` file to True and make a request to the endpoint without Authorization header. 

## Deploying to GCP
This application deploys to GCP using Cloud Build - the whole deployment is automated from a single pipeline defined in the `cloudbuild.yaml`, which runs tests, prepares runtime configuration, applies database migrations, and then deploys the service. The deployment is configured so whenever a merge into the main branch occurs the deployment pipeline starts.

### How the Cloud Build pipeline works
1. Install dependencies and run tests: `pytest tests/`.
2. Generate `app.yaml` by combining `static_app.yaml` with rendered env vars from `env_variables_template.yaml`.
3. Apply DB migrations: `flask db upgrade` and `flask db stamp head`.
4. Deploy to App Engine: `gcloud app deploy`.

The `env_variables_template.yaml` file is a template for App Engine environmental variables. During the build, `envsubst` replaces these placeholders with the real values provided to Cloud Build. The output becomes substituted_env.yaml, which is safe to generate at build time and avoids hardcoding secrets in source control.

The `static_app.yaml` file contains the static App Engine configuration that does not change between environments. At deployment, this is combined with the generated environment variables to form the final `app.yaml`.