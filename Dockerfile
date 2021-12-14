FROM python:python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /app/