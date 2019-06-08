FROM python:3.7-alpine

ENV PYTHONUNBUFFERED 1


# COPY requirements and RUN pip install BEFORE adding the rest of your code,
# this will cause Docker's caching mechanism to prevent re-installing
# (all your) dependencies when you made a change a line or two in your app.
COPY ./requirements/ /tmp/requirements/
RUN pip install -r /tmp/requirements/dev.txt

RUN mkdir /code
WORKDIR /code
ADD . /code
