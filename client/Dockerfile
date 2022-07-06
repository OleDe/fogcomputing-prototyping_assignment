FROM python:3.9.13

RUN apt-get update && apt-get install -y curl

# install zeroMQ
RUN pip install --upgrade pip
RUN pip install pyzmq pymongo bmp280

COPY client.py /client.py
COPY gather_data.py /gather_data.py

ENTRYPOINT python -u /client.py localhost
