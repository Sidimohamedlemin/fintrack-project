FROM python:3.11-slim

WORKDIR /app
COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "fintrack_project.wsgi:application", "--bind", "0.0.0.0:8000"]