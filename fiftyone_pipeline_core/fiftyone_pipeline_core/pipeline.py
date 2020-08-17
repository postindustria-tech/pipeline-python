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
    Pipeline holding a list of FlowElements for processing,
    can create FlowData that will be passed through these,
    collecting ElementData
    Should be constructed through the PipelineBuilder class

    """

    def __init__(self, flowElements, logger=Logger()):
        """
        Pipeline constructor.

        @type flowElements: list[FlowElement]
        @param flowElements: A list of flowElements

        @type logger: Logger
        @param logger: A logger to attach to the pipeline

        @rtype: Pipeline
        @returns: Returns a Pipeline

        """

        self.flowElements = flowElements

        self.logger = logger

        self.flowElementsList = {}

        for flowElement in flowElements:

            # Notify element that it has been registered in the pipeline
            flowElement.onRegistration(self)

            self.flowElementsList[flowElement.dataKey] = flowElement

            flowElement.pipelines.append(self)

    def createFlowData(self):
        """
        Create a FlowData based on what's in the pipeline
        
        @rtype: FlowData
        @returns: Return a FlowData

        """

        return FlowData(self)

    def log(self, level, message):
        """
        Log a message using the Logger.log of the pipeline's Logger.

        @type level: string
        @param level: level of log message

        @type message: string
        @param message: Returns content of log message

        """

        self.logger.log(level, message)

    def getElement(self, key):
        """
        Get a flowElement by its name.

        @type key: string
        @param key: name of flowElement

        @rtype: FlowElement
        @returns: Returns the FlowElement indicated

        """

        return self.flowElementsList[key]

    def getProperties(self):
        """
        Get all properties of all flowElements in the pipeline.

        @rtype: dict of {string : DataPropertyDictionary}
        @returns: Returns dictionary of all properties in a pipeline keyed by each flowElement's FlowElement.dataKey.

        """

        output = {}

        for flowElement in self.flowElements:
            properties = flowElement.getProperties()

            output[flowElement.dataKey] = properties

        return output
