FROM python:3.6

WORKDIR /app

RUN pip install PyMySQL

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "run.py"]
