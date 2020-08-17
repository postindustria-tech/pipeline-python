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

from .evidence_keyfilter import EvidenceKeyFilter


class FlowElement(object):
    """
    A FlowElement is placed inside a Pipeline
    It receives Evidence via a FlowData object
    It uses this to optionally create ElementData on the FlowData
    Any errors in processing are caught in the FlowData's errors object
    
    """

    def __init__(self):
        """
        List of Pipelines the FlowElement has been added to 

        """
        self.pipelines = []
        self.properties = {}
        self.dataKey = ""

    def process(self, flowData):
        """
        Function for getting the FlowElement's EvidenceKeyFilter
        Used by the filterEvidence method

        @type flowData: FlowData
        @param flowData: FlowData to be processed

        @rtype: mixed
        @returns: Returns whatever the self.processInternal method is set to return

        """

        return self.processInternal(flowData)

    def onRegistration(self, pipeline):
        """
        Function called when an element is added to the pipeline. 
        Used for example, for elements that depend on other elements in a pipeline

        @type pipeline: Pipeline
        @param pipeline: Pipeline the element has been added to

        """

        pass

    def getEvidenceKeyFilter(self):
        """
        Filter FlowData evidence using the FlowElement's EvidenceKeyFilter

        @rtype: EvidenceKeyFilter
        @returns: Returns an EvidenceKeyFilter

        """

        return EvidenceKeyFilter()

    def filterEvidence(self, flowData):
        """
        Filter FlowData evidence using the FlowElement's EvidenceKeyFilter

        @type flowData: FlowData
        @param flowData: a FlowData that has some Evidence set

        @rtype: dict
        @returns: Returns a dictionary of evidence that has passed the filter

        """

        filter = self.getEvidenceKeyFilter()

        return filter.filterEvidence(flowData.evidence.getAll())

    def filterEvidenceKey(self, key):
        """
        Filter FlowData.evidence using the flowElement's EvidenceKeyFilter
        with the property key of evidence of interest.

        @type key: string
        @param key: the property key being sought within FlowData.evidence

        @rtype: dict
        @returns: Returns a dictionary containing the property key and the evidence related to it as its value

        """

        filter = self.getEvidenceKeyFilter()

        return filter.filterEvidenceKey(key)

    def processInternal(self, flowData):
        """
        The method behind FlowElement.Process - it is called by the process() function.
        It is usually overridden by specific flowElements to do their core work.

        @type flowData: FlowData
        @param flowData: FlowData to be processed

        @rtype: bool
        @returns: Returns True

        """

        return True

    def getProperties(self):
        """
        Get the FlowElement.properties of a FlowElement.
        
        This is usually overridden by specific flowElements.

        @rtype: DataPropertyDictionary
        @returns: Returns dictionary of the FlowElement's properties

        """

        return {k.lower(): v for k, v in self.properties.items()}
