#!/usr/bin/env python3
"""
irc.py

Implements basic server to server protocol parsing

(c) andrewyu
"""

import time
import config
import logging
import link

status = {'bursted': False}


def init():
    """
    Initializes the server connection, does handshakes and such
    """
    logging.normal("irc.py: Initializing IRC")
    link.connect()
    logging.normal("irc.py: Negotiating capabilities")
    link.tx("CAPAB START 1202")
    link.tx("CAPAB CAPABILITIES :PROTOCOL=1202")
    link.tx("CAPAB END")
    link.tx(f"SERVER {config.irc_server} {config.irc_sendpass} 0 {config.irc_sid} :{config.irc_desc}")
    while True:
        line = link.rx()
        if line == "CAPAB END":
            logging.normal("irc.py: Done with capabilities")
            break
    line = link.rx()
    if line[:6] != "SERVER":
        logging.error("irc.py: Protocol violation: did not get SERVER after CAPAB END")
        exit(1)
    else:
        logging.good("irc.py: Got remote SERVER reply")
        splt = line.split(' ')
        _r_name = splt[1]
        _r_pass = splt[2]
        if _r_pass != config.irc_recvpass:
            logging.error(f"irc.py: {_r_name} is not sending correct password, got {_r_pass}")
            exit(2)
        else:
            del _r_name
            del _r_pass
            del splt
            logging.good("irc.py: Password is good")
            if not status['bursted']:
                ts = str(int(time.time()))
                link.stx("BURST")
                link.stx(f"UID {config.client_uid} {ts} {config.client_nick} {config.client_connaddr} " +
                         f"{config.client_host} {config.client_ident} {config.client_connaddr} {ts} " +
                         f"{config.client_umode} :{config.client_realname}")
                link.stx("ENDBURST")
                status['bursted'] = True
                ts = str(int(time.time()))
                link.utx(f"PRIVMSG NickServ :identify {config.client_nick} {config.client_nspass}")
                link.stx(f"FJOIN {config.log_chan} {str(int(time.time()))} + :{config.client_chmode}," +
                         f"{config.client_uid}")
                link.stx(f"FJOIN #chat {str(int(time.time()))} + :{config.client_chmode}," +
                         f"{config.client_uid}")
                link.stx(f"FJOIN #test {str(int(time.time()))} + :{config.client_chmode}," +
                         f"{config.client_uid}")
                link.stx(f"MODE {config.log_chan} +{config.client_chmode} {config.client_nick}")
            logging.normal("irc.py: IRC initialized")


stx = link.stx
utx = link.utx
tx = link.tx
rx = link.rx


if __name__ == "__main__":
    logging.error("irc.py: This library is not intended to be run")
