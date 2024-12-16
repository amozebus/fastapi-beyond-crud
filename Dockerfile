FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./startup.sh

CMD ["./startup.sh"]