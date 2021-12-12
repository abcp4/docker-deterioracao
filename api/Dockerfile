# pull official base image
FROM python:3.9.9-buster

# set working directory
WORKDIR /api/

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /api/
RUN pip install -r requirements.txt

# copy project
COPY . /api/

# run app
CMD uvicorn main:app --host 0.0.0.0 --port $PORT