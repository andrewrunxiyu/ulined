"""
akick.py

PLUGIN

Handles commands and generates replies

(c) andrewyu
"""

import logging
import config
import time
import random

#trigger = '(len(splt) >= 3 and (splt[1] == "PRIVMSG") and (splt[2] == config.client_uid and not (splt[3].startswith(' \
#          '":\x01") and splt[len(splt) - 1].endswith("\x01")))) or False'

trigger = '(len(splt) >= 3 and (splt[1] == "FJOIN"))'

def handle(irc, userlist, operlist, msg):
    """
    Main function to deal with joins
    """
    logging.normal(f"akick.py: {msg}")
    _chan = msg.split(" ")[2]
    _uid = msg.split(",")[-1]
    if _chan == "#bots":
        irc.utx(f"KICK {_chan} {_uid} :Disabled channel")
    return True
