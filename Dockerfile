FROM python:3.9-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

ENV PYTHONUNBUFFERED=1

CMD ["python", "bot.py"]
