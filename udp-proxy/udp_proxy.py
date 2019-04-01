#!/usr/bin/env python3
#
# UDP DNS to TCP DNS proxy
#
# Author: Tamer Hassan <tam.hassan7@gmail.com>
#

import socket
import threading
import socketserver

import sys
import struct
import binascii
import traceback

DST_IP = '127.0.0.1'
DST_PORT = 53
LISTEN_PORT = 53


def sendTCP(udp_query):

    tcp_query = struct.pack('>H',len(udp_query)) + udp_query

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = None

    try:
        sock.connect((DST_IP, DST_PORT))
        # print("tcp_query: "+ binascii.hexlify(tcp_query).decode())
        sock.send(tcp_query)
        data = sock.recv(1024)
        # print ("data rcvd: " + binascii.hexlify(data).decode())

    except (IOError,socket.error,Exception) as e:
        print("Socket error?")
        traceback.print_last()
        sock.close()
    finally:
        sock.close()

    return data


class ThreadedUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):
        # print("Recieved one request from {}".format(self.client_address))
        datagram = self.request[0].strip()
        # print("Datagram Recieved from client is: " + binascii.hexlify(datagram).decode())
        # print("Thread Name:{}".format(threading.current_thread().name))

        TCPreply = sendTCP(datagram)

        reqid = datagram[:2]
        response = TCPreply[4:]
        UDPreply = reqid + response

        if TCPreply:
            print("UDP reply: " + binascii.hexlify(UDPreply).decode())
            self.wfile.write(UDPreply)
        else:
            print("Invalid TCP reply!")


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass



UDPServerObject = socketserver.ThreadingUDPServer(('', LISTEN_PORT), ThreadedUDPRequestHandler)
UDPServerObject.serve_forever()
