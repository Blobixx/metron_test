FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /metron_app
WORKDIR /metron_app
COPY requirements.txt /metron_app/
RUN pip install -r requirements.txt
ADD . /metron_app/