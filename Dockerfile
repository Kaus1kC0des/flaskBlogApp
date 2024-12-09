FROM ubuntu:22.04
RUN apt-get update -y
RUN apt-get install -y python3.10 python3.10-dev python3.10-distutils build-essential python3-pip
COPY requirements.txt /app/requirements.txt
COPY flaskBlog /app/flaskBlog
COPY app.py /app/app.py
WORKDIR /app
RUN pip install -r requirements.txt
ENV PORT=5500
EXPOSE $PORT

LABEL authors="kausik"
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
#CMD ["/bin/bash"]