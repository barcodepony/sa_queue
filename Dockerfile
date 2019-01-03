FROM python:3.6
COPY . /app
WORKDIR /app
RUN pip install mysql-connector-python
EXPOSE 6000
CMD python ./app.py
