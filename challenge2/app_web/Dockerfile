FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 8002

CMD ["gunicorn", "-b 0.0.0.0:8002", "-w 4", "app:app"]
