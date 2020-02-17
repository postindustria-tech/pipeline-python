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

from .evidence import Evidence
import math

class FlowData:


    def __init__(self, pipeline):
        """
        Constructor for flowData
        :param pipeline: parent pipeline
        """

        self.data = {}
        self.errors = {}
        self.pipeline = pipeline
        self.processed = False
        self.stopped = False
        self.evidence = Evidence(self)


    def process(self):
        """
        process function runs the process function on every attached flowElement 
        allowing data to be changed based on evidence
        This can only be run once per flowData instance
        :returns flowData
        """

        if not self.processed:

            for flowElement in self.pipeline.flowElements:
                if self.stopped is not True:
                    # All errors are caught and stored in an errors array keyed by the 
                    # flowElement that set the error
 
                    try: flowElement.process(self)

                    except Exception as inst:

                        key = flowElement.dataKey

                        self.setError(key, inst)

            # Set processed flag to true. flowData can only be processed once

            self.processed = True
            return self

        else:
            self.setError("error", "FlowData already processed")



    def getFromElement(self, flowElement):
        """
        Retrieve data by flowElement object
        :param: flowElement
        :returns: elementData
        """

        try:
            return self.get(flowElement.dataKey)

        except Exception:
            return None
    


    def get(self, flowElementKey):

        """
        Retrieve data by flowElement key
        :param string: flowElementDataKey
        :returns elementData:
        """
            
        try:
            return self.data[flowElementKey.lower()]

        except Exception:
            return None



    def __getattr__(self, flowElementKey):
        """
        Magic getter to allow $flowData->flowElementKey getting 
        :param string: flowElementKey
        :returns: $elementData
        """
    
        return self.get(flowElementKey)



    def setElementData(self, data):
        """
        Set data (used by flowElement)
        :param elementData:
        """

        self.data[data.flowElement.dataKey] = data

          
    def setError(self, key, error):
        """
        Set error (should be keyed by flowElement dataKey)
        :param string: key
        :param string: error message
        """

        if key not in self.errors:
            self.errors[key] = list()
        
        self.errors[key].append(error)

        self.pipeline.log("error", error)



    def getEvidenceDataKey(self):
        """
        Get an array evidence stored in the flowData, filtered by 
        its flowElements' evidenceKeyfilters
        :returns array:
        """

        requstedEvidence = list()
        evidence = self.evidence.getAll()

        for flowElement in self.pipeline.flowElements:
            requstedEvidence = requstedEvidence.extend(flowElement.filterEvidence(self))

        return requstedEvidence

    
    def stop(self):
        """
        Stop processing any subsequent flowElements
        :returns: void
        """

        self.stopped = True


    def getWhere(self, filter):
        """
        Get data from flowElement based on property meta data
        :param string: metakey
        :param mixed: metavalue
        :returns: array
        """

        filteredPropertyDictionary = {}

        for flowElement, propertyDictionary in self.pipeline.getProperties().items():
            properties = propertyDictionary.getFiltered(filter)
            
            for dataPropertyKey in properties:
                try:
                    filteredPropertyDictionary[dataPropertyKey] = self.get(flowElement).get(dataPropertyKey)
                # We are ignoring errors in getWhere as properties could be missing on purpose
                # They shouldn't throw an error breaking the whole getWhere.
                except Exception:
                    pass

        return filteredPropertyDictionary
