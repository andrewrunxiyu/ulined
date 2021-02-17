#!/usr/bin/env python3
"""
ulined.py

Script for InspIRCd to be a ulined puppet for opers

(c) andrewyu
"""

import irc
import logging
import handler
import config

opers = []
users = {}

irc.init()

while True:
    line = irc.rx()
    if line is None:
        logging.error("uline.py: Dead socket")
        exit(3)
    splt = line.split(" ")
    if len(splt) == 4 and splt[1] == "PING":
        irc.stx("PONG " + splt[3] + " " + splt[2])
    elif len(splt) > 4 and splt[1] == "UID" and splt[4] == config.client_nick:
        irc.stx("KILL " % config.irc_sid + splt[2] + " :%s" % text_kill_nickresv)
    elif len(splt) >= 10 and splt[1] == "UID":
        users[splt[2]] = splt[4]
    elif len(splt) == 3 and splt[1] == "OPERTYPE" and splt[2] == config.oper_type:
        irc.utx(f"NOTICE {splt[0][1:]} :{config.text_operup}")
        opers.append(splt[0][1:])
    elif len(splt) >= 3 and (splt[1] == "PRIVMSG") and (splt[2] == config.client_uid and
                                                        not (splt[3].startswith(":\x01")
                                                             and splt[len(splt) - 1].endswith("\x01"))):
        if splt[0][1:] in opers:
            data = ' '.join(splt[3:])[1:]
            irc.utx("PRIVMSG %s :" % config.log_chan + users[splt[0][1:]] + " " + data)
            handler.handle(irc, users[splt[0][1:]], users, data)
            irc.utx(f"NOTICE {splt[0][1:]} :{config.text_ok}")
        else:
            irc.utx(f"NOTICE {splt[0][1:]} :{config.text_unauth}")
