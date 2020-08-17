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
import traceback


class FlowData:
    """
    FlowData is created by a specific Pipeline
    It collects evidence set by the user
    It passes evidence to FlowElements in the Pipeline
    These elements can return ElementData or populate an errors object

    """

    def __init__(self, pipeline):
        """
        FlowData constructor.

        @type pipeline: Pipeline
        @param pipeline: parent pipeline

        """

        self.data = {}
        self.errors = {}
        self.pipeline = pipeline
        self.processed = False
        self.stopped = False
        self.evidence = Evidence(self)

    def process(self):
        """
        Runs the process function on every attached flowElement allowing data to be changed based on evidence.
        This can only be run once per FlowData instance.

        @rtype: FlowData
        @return: Returns flowData

        """

        if not self.processed:

            for flowElement in self.pipeline.flowElements:
                if self.stopped is not True:
                    # All errors are caught and stored in an errors array keyed by the
                    # flowElement that set the error

                    try:
                        flowElement.process(self)

                    except Exception:

                        self.setError(flowElement.dataKey, traceback.format_exc())

            # Set processed flag to true. flowData can only be processed once

            self.processed = True
            return self

        else:
            self.setError("error", "FlowData already processed")


    def getFromElement(self, flowElement):
        """
        Retrieve data by FlowElement object.

        @type flowElement: FlowElement
        @param flowElement: FlowElement that created the data of interest

        @rtype: ElementData
        @return: Returns data that was created by the flowElement held in the FlowData

        """

        try:
            return self.get(flowElement.dataKey)

        except Exception:
            return None


    def get(self, flowElementKey):
        """
        Retrieve data by flowElement key.
        Called by FlowData.getFromElement method.

        @type flowElementKey: string
        @param flowElementKey: FlowElement.dataKey of the FlowElement that created the data of interest

        @rtype: ElementData
        @return: Returns data in the FlowData instance that is under the specified key

        """

        try:
            return self.data[flowElementKey.lower()]

        except Exception:
            return None


    def __getattr__(self, flowElementKey):
        """
        Magic getter to allow retrieval of data from FlowData.data[flowElementKey] by flowElement name.
        For example, instead of `flowdata.get("device")` you can use `flowData.device`

        @type flowElementKey: string
        @param flowElementKey: dataKey of the FlowElement that created the data of interest

        @rtype: ElementData
        
        """

        return self.get(flowElementKey)


    def setElementData(self, elData):
        """
        Set data (used by flowElement) within FlowData.data

        @type elData: ElementData
        @param elData: elementData to be added to flowData

        """

        self.data[elData.flowElement.dataKey] = elData


    def setError(self, key, error):
        """
        Set error (should be keyed by flowElement dataKey)

        @type key: string
        @param key: a flowElement.dataKey

        @type error: string
        @param error: Error message

        """

        if key not in self.errors:
            self.errors[key] = list()

        self.errors[key].append(error)

        self.pipeline.log("error", error)


    def getEvidenceDataKey(self):
        """
        Get a list of evidence stored in the flowData, filtered by
        its flowElements' evidenceKeyFilters

        @rtype: list
        @return: Returns filtered evidence

        """
        requestedEvidence = list()

        for flowElement in self.pipeline.flowElements:
            requestedEvidence = requestedEvidence.extend(flowElement.filterEvidence(self))

        return requestedEvidence


    def stop(self):
        """
        Stop processing any subsequent flowElements
        
        """

        self.stopped = True

    def getWhere(self, metaKey, metaValue):
        """
        Get data from flowElement based on property meta data

        @type metaKey: str
        @param metakey: metakey shared by all data of interest

        @type metaValue: mixed
        @param metaValue: meta value shared by all data of interest

        @rtype: dict
        @return: Returns dictionary of data created by the flowElement that have the specified meta property

        """

        metaQueryOutput = {}

        properties = self.pipeline.getProperties()

        for flowElement, flowElementProperties in properties.items():
            for propertyKey, propertyMeta in flowElementProperties.items():
                if metaKey.lower() in propertyMeta:
                    if propertyMeta[metaKey.lower()] == metaValue:
                        try:
                            metaQueryOutput[propertyKey] = self.get(flowElement).get(propertyKey)                
                        # We are ignoring errors in getWhere as properties could be missing on purpose
                        # They shouldn't throw an error breaking the whole getWhere.
                        except Exception:
                            pass
                        
        return metaQueryOutput
                        
