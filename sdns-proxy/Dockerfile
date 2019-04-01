FROM ubuntu:18.04

MAINTAINER "Tamer Hassan <tam.hassan7@gmail.com>"

RUN \
  apt-get update && \
  apt-get install -y \
    python3-twisted \
    python3-openssl \
    python3-service-identity \
    python3-idna \
    ca-certificates

WORKDIR /opt/server

COPY sdns_proxy.py /opt/server

RUN chmod a+x /opt/server/*.py

EXPOSE 53/tcp

ENTRYPOINT ["/opt/server/sdns_proxy.py"]
