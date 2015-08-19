#
# Build an image for deploying the KB
#
# To build the image:
#   docker build -t kb_server .
#
# To run the application:
#  docker run -d kb_server
#
# To find out which port to access on the host machine, run "docker ps"
# and then "docker inspect <id>"

FROM ubuntu:14.04

MAINTAINER Domenico Guarino <domenico.guarino@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --fix-missing
RUN apt-get -y -q install nginx supervisor build-essential python-dev python-setuptools python-pip sqlite3 git
RUN unset DEBIAN_FRONTEND
RUN pip install uwsgi

ADD . /home/docker/site

RUN pip install -r /home/docker/site/deployment/requirements.txt

WORKDIR /home/docker/site
ENV PYTHONPATH  /home/docker:/usr/local/lib/python2.7/dist-packages

# (remove if exists and) create sqlite db
RUN if [ -f /home/docker/site/db.sqlite3 ]; then rm /home/docker/site/db.sqlite3; fi
RUN python manage.py migrate --noinput
RUN python manage.py initadmin
RUN python manage.py collectstatic --noinput # copy all static files into the nginx-served static folder
RUN unset PYTHONPATH

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /home/docker/site/deployment/nginx-app.conf /etc/nginx/sites-enabled/
RUN ln -s /home/docker/site/deployment/supervisor-app.conf /etc/supervisor/conf.d/
RUN ln -sf /dev/stdout /var/log/nginx/access.log
RUN ln -sf /dev/stderr /var/log/nginx/error.log

RUN chmod -R a+rx maps/
RUN chmod -R a+rx stmtdb/
RUN chmod -R a+rx templates/
RUN chmod -R a+rx static/

ENV PYTHONPATH /usr/local/lib/python2.7/dist-packages:/usr/lib/python2.7/dist-packages
EXPOSE 80
CMD ["supervisord", "-n"]
