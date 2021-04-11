FROM python:3.8

WORKDIR /app

EXPOSE 8080

COPY . .

RUN pip3 install -r requirments.txt

RUN chmod +x weight_run.sh

ENTRYPOINT ["./weight_run.sh"]
