FROM python:3.6-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
ENV PORT=8080
ENV HOST=0.0.0.0

COPY . .

ENTRYPOINT ["python"]

CMD ["run.py"]


