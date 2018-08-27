FROM python:2.7-alpine

WORKDIR /var/app

COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .
