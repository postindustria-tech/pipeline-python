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
    def __init__(self, flowElements, logger=Logger()):
        """
        Pipeline constructor
        param: array list of flowElements
        param: array settings array
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
        createFlowData - Create a flowData based on what's in the pipeline
        
        returns: FlowData
        """

        return FlowData(self)

    def log(self, level, message):

        self.logger.log(level, message)

    def getElement(self, key):
        """
        getElement - Get a flowElement by its name
        param: String name
        returns: flowElement
        """

        return self.flowElementsList[key]


    def getProperties(self):

        # Loop over all of self.flowElements, run getProperties() on all of them to get a dictionary 
        # And merge all of these dictionaries into one

        output = {}

        for flowElement in self.flowElements:
            properties = flowElement.getProperties()

            output[flowElement.dataKey] = properties

        return output
