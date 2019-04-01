#!/usr/bin/env python3
#
# TCP DNS to DNS-over-TLS proxy
#
# Author: Tamer Hassan <tam.hassan7@gmail.com>
#

import sys

from twisted.internet import reactor, ssl
from twisted.internet.protocol import Protocol, DatagramProtocol, Factory, ClientFactory, ServerFactory
from twisted.names import client, dns, server
from twisted.python import log


DST_IP = '1.1.1.1'
DST_PORT = 853
DST_SSL_HOSTNAME = 'cloudflare-dns.com'

class TCPServer(Protocol):
    def __init__(self):
        self.buffer = None
        self.dns_proxy_protocol = None

    def connectionMade(self):
        tls_dns_client_factory = ClientFactory()
        tls_dns_client_factory.protocol = TCPProxyServer
        tls_dns_client_factory.server = self

        certOptions = ssl.optionsForClientTLS(hostname=DST_SSL_HOSTNAME)
        reactor.connectSSL(DST_IP, DST_PORT,
                            tls_dns_client_factory,
                            certOptions)
                            # ssl.CertificateOptions())

    def dataReceived(self, data):
        if self.dns_proxy_protocol:
            self.dns_proxy_protocol.write(data)
        else:
            self.buffer = data

    def write(self, data):
        self.transport.write(data)


class TCPProxyServer(Protocol):
    def connectionMade(self):
        self.factory.server.dns_proxy_protocol = self
        self.write(self.factory.server.buffer)
        self.factory.server.buffer = ''

    def dataReceived(self, data):
        self.factory.server.write(data)

    def write(self, data):
        if data:
            self.transport.write(data)


serverFactory = ServerFactory()
serverFactory.protocol = TCPServer

# log.startLogging(sys.stdout)

reactor.listenTCP(53, serverFactory)
reactor.run()
