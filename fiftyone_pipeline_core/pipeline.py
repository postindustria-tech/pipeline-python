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

from .flowdata import FlowData
from .logger import Logger


class Pipeline:
    """
    An immutable collection of FlowElements
    to enable the user to do all the processing they require on `FlowData` with a single call.
    """

    def __init__(self, flowElements, logger=Logger()):
        """
        Pipeline constructor.

        :param flowElements: array list of flowElements
        :type flowElements: list
        :param logger: settings for a logger
        :type logger: list of tuples
        :returns: a Pipeline
        :rtype: :class: `Pipeline` instance
        """

        self.flowElements = flowElements

        self.logger = logger

        self.log("info", "test")

        self.flowElementsList = {}

        for flowElement in flowElements:

            self.flowElementsList[flowElement.dataKey] = flowElement

            flowElement.pipelines.append(self)

    def createFlowData(self):
        """
        Create a `FlowData` based on what's in the pipeline
        
        :returns: a FlowData
        :rtype: :class: `FlowData` instance
        """

        return FlowData(self)

    def log(self, level, message):
        """
        Log a message using the `Logger.log` :method: of the pipeline's Logger.

        :param level: level of log message
        :type level: string
        :param message: content of log message
        :type message: string
        """

        self.logger.log(level, message)

    def getElement(self, key):
        """
        Get a flowElement by its name.

        :param key: name of flowElement
        :type key: string
        :returns: the :class:`FlowElement` instance indicated
        :rtype: `FlowElement`
        """

        return self.flowElementsList[key]

    def getProperties(self):
        """
        Get all properties of all flowElements in the pipeline.

        Loop over all of `self.flowElements`:instance_attribute:, run `FlowElement.getProperties()`:method: on all of them to get a dictionary. 
        And merge all of these dictionaries into one.

        :returns: a dictionary of all properties in a pipeline keyed by each flowElement's `FlowElement.dataKey`:instance_attribute: .
        :rtype: dict
        """

        output = {}

        for flowElement in self.flowElements:
            properties = flowElement.getProperties()

            output[flowElement.dataKey] = properties

        return output
