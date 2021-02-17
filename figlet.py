"""
ulined.py

Script for InspIRCd to be a ulined puppet for opers

(c) bigfoot547, andrewyu
"""

import socket
import time
import config

netadmins = []
users = {}


def write(sock, line):
    if len(line) < 10 or line[5:9] != "PONG":
        print(config.data_out + repr(line)[1:-1])
    sock.sendall((line + "\n").encode("utf-8"))


def read(file):
    line = file.readline()
    if line is None or line == "":
        return None

    line = line.strip("\n")
    if len(line) < 10 or line[5:9] != "PING":
        print(config.data_in + repr(line)[1:-1])
    return line


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((config.host, config.port))
    file = sock.makefile(errors='replace')
    write(sock, "CAPAB START 1202")
    write(sock, "CAPAB CAPABILITIES :PROTOCOL=1202")
    write(sock, "CAPAB END")
    write(sock, "SERVER %s %s 0 %s :%s" % (config.servername, config.sendpass, config.sid, config.serverdesc))

    bursted = False
    while True:
        line = read(file)
        if line is None:
            print(config.sock_dead)
            exit()
        elif line[:6] == "SERVER" and not bursted:
            write(sock, ":%s BURST" % config.sid)
            write(sock, ":%s ENDBURST" % config.sid)
            bursted = True
            write(sock, ":%s UID %s %s %s %s %s %s %s %s %s :%s" % (
            config.sid, config.uid, int(time.time()), config.nick, config.connaddr, config.servername, config.ident,
            config.connaddr, int(time.time()), config.umode, config.realname))
            write(sock, ":%s FJOIN %s 1527724153 + :o,%s" % (config.sid, config.logchan, config.uid))
        splt = line.split(" ")
        if len(splt) == 4 and splt[1] == "PING":
            write(sock, ":%s PONG " % config.sid + splt[3] + " " + splt[2])
        elif len(splt) > 2 and splt[1] == "UID" and splt[4] == config.nick:
            write(sock, ":%s KILL " % config.sid + splt[2] + " :%s" % text_kill_nickresv)
        elif len(splt) >= 4 and (splt[1] == "PRIVMSG"):
            if splt[2] == config.uid and not (splt[3].startswith(":\x01") and splt[len(splt) - 1].endswith("\x01")):
                if splt[0] in netadmins:
                    cmd = ' '.join(splt[3:])[1:]
                    write(sock, cmd)
                    write(sock, ":%s PRIVMSG %s :" % (config.uid, config.logchan) + users[splt[0][1:]] + " " + cmd)
                    write(sock, ":%s %s " % (config.uid, config.msg) + splt[0][1:] + " :%s" % config.text_ok)
                else:
                    write(sock, ":%s %s " % (config.uid, config.msg) + splt[0][1:] + " :%s" % config.text_unauth)
        elif str('OPERTYPE %s' % config.opertype) in line:
            write(sock, ":%s %s " % (config.uid, config.msg) + splt[0][1:] + " :%s" % config.text_operup)
            netadmins.append(splt[0])
        elif splt[1] == "UID":
            users[splt[2]] = splt[4]
            write(sock, ":%s PRIVMSG %s :" % (config.uid, config.logchan) + "User %s %s" % (splt[2], splt[4]))
