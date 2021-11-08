FROM python:3.7-slim-buster

COPY ./requirements.txt /requirements.txt
RUN pip3 install pip==20.2.4
RUN pip3 install -r /requirements.txt

COPY ./tzfinderapi /tzfinderapi
COPY ./run.sh /run.sh

CMD /run.sh