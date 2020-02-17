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

from .pipeline import Pipeline
from .logger import Logger
import json

class PipelineBuilder:
    """
    Used to construct instances of the Pipeline. This class follows the fluent builder pattern. 

    Can take a FlowElement and add it as a direct child of the Pipeline.

    Can add a Logger to the Pipeline.

    Builds a Pipeline. Flow elements (and Engines) and Loggers are always executed sequentially in the order they were added.

    Returns the completed Pipeline.
    """

    def __init__(self):

        self.flowElements = []
        self.logger = Logger()

    def add(self, flowElement):
        """
        Add flowElement to be used in pipeline
        
        :param flowElement: flowElement to be added to the pipeline

        :type flowElement: object 
        """

        self.flowElements.append(flowElement)

        return self



    def build(self):
        """
        build - Build pipeline once done
        return: pipeline
        """

        return Pipeline(self.flowElements, logger=self.logger)



    def addLogger(self, logger):
        """
        addLogger - Add an instance of the logger class to the pipeline
        param: logger
        returns: pipeline
        """

        self.logger = logger

        return self



    def buildFromConfig(self, file):
        # TODO
        pass

