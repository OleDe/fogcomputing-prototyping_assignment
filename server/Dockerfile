FROM python:3.9.13

# install zeroMQ
RUN pip install --upgrade pip
RUN pip install pyzmq

COPY server.py /server.py

ENTRYPOINT python -u /server.py
