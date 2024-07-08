FROM python:3.10

WORKDIR /var/www

COPY /requirements.txt .
RUN pip install -r /var/www/requirements.txt
COPY /project .


CMD ["fastapi", "run", "main.py","--port", "8000"]

