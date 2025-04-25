FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./manage.py /app/manage.py
COPY ./generate_secret_key.py /app/generate_secret_key.py
COPY ./.env.template /app/.env.template
COPY ./nginx/ /app/nginx
COPY ./config/ /app/config
COPY ./users/ /app/users
COPY ./.env /app/.env
COPY ./ads/ /app/ads
COPY ./static/ /app/static

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
