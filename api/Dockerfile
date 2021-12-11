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

# exposes the port 8000 to outside wold.
EXPOSE 8000

# run app
ENTRYPOINT [ "uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]