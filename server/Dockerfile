FROM python:3.9.13

# install zeroMQ
RUN pip install --upgrade pip
RUN pip install pyzmq pymongo

COPY server.py /server.py
COPY db.py /db.py

ENTRYPOINT python -u /server.py
