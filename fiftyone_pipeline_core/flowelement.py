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

from .dataproperty_dictionary import DataPropertyDictionary
from .flowdata import FlowData
from .evidence_keyfilter import EvidenceKeyFilter


class FlowElement(object): 

    def __init__(self):
        
        self.pipelines = []
        self.properties = {} 
        self.dataKey = ""
    
    def process(self, flowData):
        """
        process: General wrapper function that calls a flowElement's processInternal method     
        param: flowData
        """

        return self.processInternal(flowData)



    def getEvidenceKeyFilter(self):
        """
        getEvidenceKeyFilter - Function for getting the flowElement's evidenceKeyFilter
        Used by the filterEvidence method
        returns: evidenceKeyFilter
        """

        return EvidenceKeyFilter()

 

    def filterEvidence(self, flowData):
        """
        filterEvidence - Filter flowData evidence using the flowElement's evidenceKeyFilter
        param: flowData
        returns: mixed
        """

        filter = self.getEvidenceKeyFilter()

        return filter.filterEvidence(flowData.evidence.getAll())



    def filterEvidenceKey(self, key):
        """
        filterEvidenceKey - Filter flowData evidence using the flowElement's evidenceKeyFilter
        param: flowData
        returns: mixed
        """

        filter = self.getEvidenceKeyFilter()

        return filter.filterEvidenceKey(key)

 

    def processInternal(self, flowData):
        """
        processInternal - Process flowData - this is process function
        is usually overriden by specific flowElements to do their core work
        param: flowData
        """

        return True

    

    def getProperties(self):
        """
        getProperties - Get properties is usually overriden by specific flowElements
        returns $
        """

        if self.properties is not None:
            return self.properties
        else:
            return DataPropertyDictionary(self)

