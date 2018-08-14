FROM python:2.7-alpine

WORKDIR /var/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt 

CMD ["python", "main.py"]
