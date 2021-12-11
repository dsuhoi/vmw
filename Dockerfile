FROM tiangolo/uwsgi-nginx:python3.8
MAINTAINER dsuhoi "dsuh0i.h8@gmail.com"
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev
COPY ./requirements.txt /requirements.txt
WORKDIR /
RUN pip3 install -r requirements.txt
COPY . /
ENTRYPOINT [ "python3" ]
CMD [ "manage.py runserver" ]
