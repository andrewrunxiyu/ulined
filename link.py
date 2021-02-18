#!/usr/bin/env python3
"""
link.py

Starts sockets for communication

(c) andrewyu
"""

import logging
import socket
import config
import ssl


# Variable for storing connection objects
# (socket, socket_file)
connection = ()


def rx():
    """
    Reads text from a socket
    """
    cfile = connection[1]
    data = cfile.readline()
    if data is None or data == "":
        return None
    data = data.strip("\n")
    logging.rx(data)
    return data


def tx(data):
    """
    Sends text to a socket
    """
    conn = connection[0]
    conn.sendall((data + "\n").encode("utf-8"))
    logging.tx(data)


def stx(data):
    """
    Prefixes data with :sid and sends it
    """
    tx(":" + config.irc_sid + " " + data)


def utx(data):
    """
    Prefixes data with :uid and sends it
    """
    tx(":" + config.client_uid + " " + data)


def connect(host=config.link_host, port=config.link_port):
    """
    Connects to a server, using config.link_host and config.link_port by default
    """
    logging.normal(f"link.py: Connecting to {host} {port}")
    sock = socket.create_connection((host, port))
    logging.good("link.py: Connection seems to be established")
    if config.link_ssl:
        ssl_context = ssl.create_default_context()
        conn = ssl_context.wrap_socket(sock, server_hostname=host)
    else:
        conn = sock
    cfile = conn.makefile(errors="repalce")
    global connection
    connection = (conn, cfile)


if __name__ == "__main__":
    logging.error("link.py: This library is not intended to be run")
