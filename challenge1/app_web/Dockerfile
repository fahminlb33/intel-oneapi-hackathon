FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . /app

RUN set -eux; \
	apt-get update; \
	apt-get install -y --no-install-recommends curl; \
	rm -rf /var/lib/apt/lists/*

EXPOSE 8001

CMD ["gunicorn", "--log-level", "debug", "--bind", "0.0.0.0:8001", "--workers", "4", "app:app"]
