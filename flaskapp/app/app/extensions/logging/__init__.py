import logging
import os


class Logging:

    def __init__(self, app_instance):
        if app_instance:
            self.init_app(app_instance)

    def init_app(self, app):
        LOGFILE = "logs.log"
        logging.basicConfig(level=logging.DEBUG,
                            format="[%(asctime)s]: {} %(levelname)s %(message)s".format(os.getpid()),
                            datefmt="%Y-%m-%d %H:%M:%S",
                            handlers=[logging.FileHandler(LOGFILE)],
                            # filename=
                            )
        app.logger = logging
# Four components of a logger: Handler: Direct events to right destination defaults to stream handler which
# directs logging to the terminal pythons runs on
# Filter: Transform event or writes it
# Formatter: Used to specify the layout of messages when logger writes them
# logger exposes the interface that application code directly uses.

# We can configure logger at different modules or class to have finer grain control over python logs

# General Information to log: Timestamp, Event Context, Severity Level
# python defines Critical, Error, Warning, Info and Debug level. Logs are only out put if is warning or worse
