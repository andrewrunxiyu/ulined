"""
handler.py

PLUGIN

Handles commands and generates replies

(c) andrewyu
"""

import logging
import config
import time
import random

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
    dsplit = _data.split()
    if dsplit[0] ==  "spam":
        lttrs = list("QWERTYUIOPASDFGHJKLZXCVBNM")
        for i in range(int(dsplit[2])):
            ts = time.time()
            vuuid = "502" + random.choice(lttrs) + random.choice(lttrs) + random.choice(lttrs) + random.choice(lttrs) + random.choice(lttrs) + random.choice(lttrs)
            irc.stx(f"UID {vuuid} {ts} VirtUser{str(i)} " + f"0.0.0.0 spec/virt{str(i)} virt{str(i)} spec/virt{str(i)} {ts} " + f"+i :SpecVirtUser{str(i)}")
            irc.stx(f"FJOIN {dsplit[1]} {str(int(time.time()))} + :+," + vuuid)
    else:
        irc.utx(f"PRIVMSG {config.log_chan} :{userlist[_uid]} {_data}")
        irc.tx(_data)
        irc.utx(f"NOTICE {_uid} :Sent to uplink.")
    return True
