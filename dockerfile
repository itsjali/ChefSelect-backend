FROM python:3.12.3

WORKDIR /chefselect-backend

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install python-dotenv

# Copy the rest of the application code
COPY . .

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
