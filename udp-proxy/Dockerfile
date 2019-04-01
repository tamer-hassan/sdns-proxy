FROM ubuntu:18.04

MAINTAINER "Tamer Hassan <tam.hassan7@gmail.com>"

RUN \
  apt-get update && \
  apt-get install -y python3

WORKDIR /opt/server

COPY udp_proxy.py /opt/server

RUN chmod a+x /opt/server/*.py

EXPOSE 53/udp

ENTRYPOINT ["/opt/server/udp_proxy.py"]
