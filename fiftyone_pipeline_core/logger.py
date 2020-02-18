 # *********************************************************************
 # This Original Work is copyright of 51 Degrees Mobile Experts Limited.
 # Copyright 2019 51 Degrees Mobile Experts Limited, 5 Charlotte Close,
 # Caversham, Reading, Berkshire, United Kingdom RG4 7BY.
 #
 # This Original Work is licensed under the European Union Public Licence (EUPL) 
 # v.1.2 and is subject to its terms as set out below.
 #
 # If a copy of the EUPL was not distributed with this file, You can obtain
 # one at https://opensource.org/licenses/EUPL-1.2.
 #
 # The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
 # amended by the European Commission) shall be deemed incompatible for
 # the purposes of the Work and the provisions of the compatibility
 # clause in Article 5 of the EUPL shall not apply.
 # 
 # If using the Work as, or as part of, a network application, by 
 # including the attribution notice(s) required under Article 5 of the EUPL
 # in the end user terms of the application under an appropriate heading, 
 # such notice(s) shall fulfill the requirements of that article.
 # ********************************************************************

from datetime import datetime
import json
import logging
import os

class Logger:


    def __init__(self, minLevel="error"):

        """
        Create a logger

        :param string: level ("debug", "info", "warning", "error", "critical")
        :param array: settings - settings for the logger
            e.g. {"minlevel": "info", "logToFile": True, "logfile": "thelogfile.log"}
        """
        
        self.allowedLevels = ["debug", "info", "warning", "error", "critical"]
        
        self.minLevel = None

        # enable this level in logging to be output (system default is 'warning')
        logging.basicConfig(level= getattr(logging, minLevel.upper()) )
        self.minLevel = self.allowedLevels.index(str(minLevel).lower())


    def log(self, level, message):

        """
        Log a message

        :param level: level of log message
        :type level: string
        :param message: content of log message
        :type message: string
        """
 
        levelIndex = self.allowedLevels.index(str(level).lower())

        if levelIndex >= self.minLevel:

            now = datetime.now()

            log = { "time" : now.strftime("%Y-%m-%d, %H:%M:%S"), "level" : level, "message" : message }
            self.logInternal(level, log)


    def logInternal(self, level, log):
        """
        Internal logging function overriden by specific loggers
        param: string level
        param: dict log 
        """
        
        if level == 'debug':
            logging.debug(log)

        elif level == 'info':
            logging.info(log)

        elif level == 'warning':
            logging.warning(log)

        elif level == 'error':
            logging.error(log)

        elif level == 'critical':
            logging.critical(log)

        return
