"""
handler.py

PLUGIN

Handles commands and generates replies

(c) andrewyu
"""

import logging
import config

trigger = 'len(splt) >= 3 and (splt[1] == "PRIVMSG") and (splt[2] == config.client_uid and not (splt[3].startswith(' \
          '":\x01") and splt[len(splt) - 1].endswith("\x01")))'


def raw(irc, msg):
    """
    Give raw commands to the uplinked server
    """
    irc.tx(msg)


def handle(irc, userlist, operlist, msg):
    """
    Main function to deal with commands in PRIVMSGs
    """
    logging.normal(f"handler.py: {msg}")
    splt = msg.split()
    _uid = splt[0][1:]
    _data = ' '.join(splt[3:])[1:]
    _nick = userlist[_uid]
    if _uid not in operlist:
        irc.utx(f"NOTICE {_uid} :You are not authorized to use {config.client_nick}.")
        return True
    irc.utx(f"PRIVMSG {config.log_chan} :{userlist[_uid]} {_data}")
    irc.tx(_data)
    irc.utx(f"NOTICE {_uid} :Done.")
    return True
