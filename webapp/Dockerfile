FROM python:3.9.9-buster

WORKDIR /app/

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]

CMD ["app.py"]