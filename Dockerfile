FROM python:3.7-slim-buster

# Copy and install the api
WORKDIR /usr/src/app
RUN pip3 install pip==20.2.4
COPY tzfinderapi/ tzfinderapi
COPY setup.py setup.py
COPY setup.cfg setup.cfg
RUN pip3 install .

# Copy the entrypoint script that will run uvicorn
COPY ./run.sh /run.sh

CMD /run.sh