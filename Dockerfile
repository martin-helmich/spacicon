FROM python:3.6

COPY requirements.txt /requirements.txt
RUN  pip install -r /requirements.txt

COPY . /opt/app

WORKDIR /opt/app
ENV FLASK_APP=server.py

CMD  ["flask", "run", "--host", "0.0.0.0"]
