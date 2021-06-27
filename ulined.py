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

def run():
    try:

        opers = []
        users = {}
        plugins = []

        logging.normal("ulined.py: Loading plugins")
        for _plugin in config.plugins_enabled:
            exec(f"import {_plugin}")
            plugins.append(eval(_plugin))
        logging.good("ulined.py: Plugins loaded")

        irc.init()
        while True:
            line = irc.rx()
            if line is None:
                logging.error("uline.py: Dead socket")
                raise Exception("Dead socket")
            done = False
            splt = line.split(" ")
            for plugin in plugins:
                if eval(plugin.trigger):
                    done = plugin.handle(irc, users, opers, line)
                    if done:
                        continue
            if done:
                continue
            if len(splt) == 4 and splt[1] == "PING":
                irc.stx("PONG " + splt[3] + " " + splt[2])
            elif len(splt) > 4 and splt[1] == "UID" and splt[4] == config.client_nick:
                irc.stx("KILL " + splt[2] + " :%s" % text_kill_nickresv)
            elif len(splt) >= 10 and splt[1] == "UID":
                users[splt[2]] = splt[4]
            elif len(splt) == 3 and splt[1] == "OPERTYPE" and splt[2] == config.oper_type:
#                irc.utx(f"NOTICE {splt[0][1:]} :{config.text_operup}")
                opers.append(splt[0][1:])
    except Exception as e:
        #logging.error(f"ulined.py: Unexpected error: {type(e)} {str(e)}")
        raise
        exit(255)
    except KeyboardInterrupt:
        logging.bad("ulined.py: Got SIGINT, quitting")
        exit(0)

if __name__ == "__main__":
    while True:
        run()
