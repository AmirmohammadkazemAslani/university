FROM python:3.10

WORKDIR /var/www

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt
COPY ./project /var/www/project
COPY ./static /var/www/static
COPY ./templates /var/www/templates


CMD ["fastapi", "run", "project.main.py","--port", "8000"]

