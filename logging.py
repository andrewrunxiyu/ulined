"""
logging.py

Simple library to log some stuff

(c) andrewyu
"""

import config


def output(data):
    """
    Command to handle outputs
    """
    print(data)


def error(data):
    """
    Logs a error
    """
    output(config.log_prefix_error + data)


def normal(data):
    """
    Logs a normal log
    """
    output(config.log_prefix_normal + data)


def good(data):
    """
    Logs a good log
    """
    output(config.log_prefix_good + data)


def bad(data):
    """
    Logs a bad log
    """
    output(config.log_prefix_bad + data)


def tx(data):
    """
    Logs transmits
    """
    output(config.log_prefix_tx + data)


def rx(data):
    """
    Logs receives
    """
    output(config.log_prefix_rx + data)


if __name__ == "__main__":
    logging.error("logging.py: This library is not intended to be run. ")
