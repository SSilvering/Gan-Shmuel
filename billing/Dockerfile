FROM python:3.6

WORKDIR /app

RUN pip install PyMySQL

COPY requirements.txt .

RUN pip install -r requirements.txt
ENV PORT=5000
ENV HOST=0.0.0.0


COPY . .

CMD ["python", "run.py"]
