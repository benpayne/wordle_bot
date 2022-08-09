FROM python:3.8

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY c_extension /tmp/c_extension
COPY setup.py /tmp

WORKDIR /tmp
RUN python3 setup.py install 

COPY flask-server /app
WORKDIR /app

EXPOSE 80

ENV STATIC_PATH /app/app/static
ENV STATIC_URL /static

CMD ["gunicorn", "--conf", "app/gunicorn.py", "-b", "0.0.0.0", "app:app"]