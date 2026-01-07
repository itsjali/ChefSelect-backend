FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

RUN pip install python-dotenv

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
