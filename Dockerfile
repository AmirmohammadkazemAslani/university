FROM python:3.10

WORKDIR /var/www

COPY /requirements.txt .
RUN pip install -r requirements.txt
COPY /project .


CMD ["fastapi", "run", "main.py","--port", "8000"]

