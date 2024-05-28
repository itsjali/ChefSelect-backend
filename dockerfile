FROM python:3.9-slim

WORKDIR /chefselect-backend

COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 5000

ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
