FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY c_extension /tmp/c_extension
COPY setup.py /tmp

WORKDIR /tmp
RUN python3 setup.py install 

COPY flask-server /app
WORKDIR /app

ENV STATIC_PATH /app/app/static
