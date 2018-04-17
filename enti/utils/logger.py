# -*- coding: utf-8 -*-

import logging
from pprint import pformat
import colorama


class Logger:

    def __init__(self):
        self.stream = None
        self.dw_log = None

        colorama.init()
        self.init_stream()

    def init_stream(self):
        """Configures stream messaging"""

        # Get the logger
        self.stream = logging.getLogger('canary-stream')

        # Prevent duplicate messages
        self.stream.propagate = False

        # Set logger level
        self.stream.setLevel(logging.DEBUG)

        # Add the stream handler
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.stream.addHandler(stream_handler)

    def colorize(self, string, style=None):
        """
        Colorize stream output

        :param string: string
        :param style: style
        :return: formatted string
        """
        styles = {
            "RED": colorama.Fore.RED,
            "YELLOW": colorama.Fore.YELLOW,
            "GREEN": colorama.Fore.GREEN,
            "BLACK": colorama.Style.DIM,
            "DIM": colorama.Style.DIM
        }
        if style is None:
            style = string

        return '{}{}{}'.format(styles[style], string, colorama.Style.RESET_ALL)

    def debug(self, m, extra=None, stream=True):
        """
        Logs a `debug`-level message

        :param m: message
        :param extra: dict of extra variables
        :return: None
        """
        if stream:
            if extra is None:
                self.stream.debug(m)
            else:
                self.stream.debug('{}\n{}\n'.format(m, pformat(extra)))


    def info(self, m, extra=None, stream=True):
        """
        Logs an `info`-level message

        :param m: message
        :param extra: dict of extra variables
        :return: None
        """
        if stream:
            if extra is None:
                self.stream.info(m)
            else:
                self.stream.info('{}\n{}\n'.format(m, pformat(extra)))


    def warn(self, m, extra=None, stream=True):
        """
        Logs a `warning`-level message

        :param m: message
        :param extra: dict of extra variables
        :return: None
        """
        if stream:
            if extra is None:
                self.stream.warn(m)
            else:
                self.stream.warn('{}\n{}\n'.format(m, pformat(extra)))

    def error(self, m, extra=None, stream=True):
        """
        Logs an `error`-level message

        :param m: message
        :param extra: dict of extra variables
        :return: None
        """
        if stream:
            if extra is None:
                self.stream.error(m)
            else:
                self.stream.error('{}\n{}\n'.format(m, pformat(extra)))


    def exception(self, e):
        """
        Logs an `error`-level message

        :param e: exception
        """
        self.stream.exception(e)
