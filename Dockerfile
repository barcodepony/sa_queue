FROM python:3.6
COPY . /app
WORKDIR /app
EXPOSE 6000
CMD python ./app.py
