FROM sgsullivan/python3-django-postgres-celery-rabbitmq:latest

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get dist-upgrade -y && apt-get install -y openssh-server

RUN mkdir /var/run/sshd

COPY sshd_config /etc/ssh/

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]
