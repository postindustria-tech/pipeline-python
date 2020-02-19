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
from .evidence_keyfilter import EvidenceKeyFilter


class FlowElement(object):
    """A black box that accepts Flow Data and performs some operation.
    It may or may not populate the Flow Data with Aspect property values."""

    def __init__(self):
        """Initialise construction of FlowElement """
        self.pipelines = []
        self.properties = {}
        self.dataKey = ""

    def process(self, flowData):
        """
        General wrapper function that calls a FlowElement's FlowElement.processInternal method

        :param flowData: FlowData to be processed
        :type flowData: FlowData
        :returns: whatever the `self.processInternal` method is set to return
        :rtype: mixed
        """

        return self.processInternal(flowData)

    def getEvidenceKeyFilter(self):
        """
        Function for getting a FlowElement's EvidenceKeyFilter.

        Used by FlowElement.filterEvidence method
        :returns: an EvidenceKeyFilter
        :rtype: EvidenceKeyFilter
        """

        return EvidenceKeyFilter()

    def filterEvidence(self, flowData):
        """
        Filter FlowData.evidence using the flowElement's EvidenceKeyFilter

        :param flowData: a FlowData that has some `Evidence` set
        :type flowData: FlowData
        :returns: a dictionary of evidence that has passed the filter
        :rtype: dict
        """

        filter = self.getEvidenceKeyFilter()

        return filter.filterEvidence(flowData.evidence.getAll())

    def filterEvidenceKey(self, key):
        """
        Filter `FlowData.evidence`:instance_attribute: using the flowElement's `EvidenceKeyFilter`
        with the property key of evidence of interest.

        :param key: the property key being sought in the `FlowData.evidence`:instance_attribute: 
        :returns: a dictionary containing the property key and the evidence related to it as it's value
        :rtype: dict
        """

        filter = self.getEvidenceKeyFilter()

        return filter.filterEvidenceKey(key)

    def processInternal(self, flowData):
        """
        The method behind `FlowElement.Process`:method: - it is called by the process() function.
        It is usually overridden by specific flowElements to do their core work.

        :param flowData: FlowData to be processed
        :type flowData: :class:`FlowData` instance
        :returns: True
        """

        return True

    def getProperties(self):
        """
        Get the `FlowElement.properties`:instance_attribute: of a :class:`FlowElement` instance. 
        
        This is usually overridden by specific flowElements.
        :returns: dictionary of the `FlowElement`s properties
        :rtype: `DataPropertyDictionary`:class: dict instance
        """

        if self.properties is not None:
            return self.properties
        else:
            return DataPropertyDictionary(self)
