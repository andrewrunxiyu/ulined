"""
handler.py

Handles commands and generates replies

(c) andrewyu
"""


def handle(irc, uid, userlist, msg):
    """
    Main function to deal with commands in PRIVMSGs
    """
    irc.tx(msg)
