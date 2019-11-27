FROM python:3.7

LABEL image for a very simple flask application

WORKDIR  /backend

COPY . /backend

RUN pip install -r requirements.txt

RUN export FLASK_DEBUG=1

CMD python ./app.py
