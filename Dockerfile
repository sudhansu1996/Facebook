FROM python:3.8-slim-buster

WORKDIR /app.py

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
 
COPY . .


CMD [ "python3", "app.py"]