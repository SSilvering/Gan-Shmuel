FROM python:3.8 AS builder
COPY requirements.txt .

RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.8-alpine
WORKDIR /app

COPY --from=builder /root/.local /usr/local
COPY . .

ENV PORT=5000
ENV DEBUG=True

EXPOSE 5000

ENTRYPOINT [ "python" ]
CMD [ "./run.py" ]