FROM python:3.9

WORKDIR /usr/src/trol

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "makemigrations" && "python", "manage.py", "migrate" && "python", "manage.py", "runserver", "0.0.0.0:8000"]
