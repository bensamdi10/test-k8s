# coding: utf-8
import socket
import argparse
import threading
import os
import requests

parser = argparse.ArgumentParser(description = "This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = socket.gethostname())
parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = 42569)
args = parser.parse_args()

NUMBER_PEER = 5
sck = socket.socket()

def startSoket():
    sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sck.bind((args.host, args.port))
        sck.listen(NUMBER_PEER)
    except Exception as e:
        raise SystemExit("We could not bind the server on host: {args.host} to port: {args.port}, because: {e}")




def onNewClient(client, connection):
    ip = connection[0]
    port = connection[1]
    print("THe new connection was made from IP: {ip}, and port: {port}!")
    while True:
        msg = client.recv(1024)
        if msg.decode() == 'exit':
            break
        print("The client said: {msg.decode()}")
        reply = "You told me: {msg.decode()}"
        client.sendall(reply.encode('utf-8'))
    print("The client from ip: {ip}, and port: {port}, has gracefully diconnected!")
    client.close()


 while True:
        try:
            client, ip = sck.accept()
            threading._start_new_thread(onNewClient, (client, ip))
        except KeyboardInterrupt:
            print("Gracefully shutting down the server!")
        except Exception as e:
            print("Well I did not anticipate this: {e}")
