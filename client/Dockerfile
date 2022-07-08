FROM python:3.9.13

# install zeroMQ
RUN pip install --upgrade pip
RUN pip install pyzmq pymongo

COPY client.py /client.py
COPY gather_data.py /gather_data.py
COPY db.py /db.py

ENTRYPOINT python -u /client.py
