FROM python:3.10-alpine
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev
RUN python -m pip install --upgrade pip
RUN mkdir /app
RUN addgroup -S app && adduser -S app -G app
RUN mkdir /app/assets
RUN mkdir /app/media
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY entrypoint.sh /app/
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
COPY . /app/

ENTRYPOINT ["/app/entrypoint.sh"]