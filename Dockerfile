FROM python:slim
WORKDIR /service
COPY . .
RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT sleep 60 && python __main__.py