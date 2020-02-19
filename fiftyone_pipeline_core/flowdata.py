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


class FlowData:
    """A user facing data object containing both the evidence, and the Aspect properties based on the evidence.

    :attribute Evidence: Data that a web application receives as part of a web request.

    An Aspect refers to a discrete item of interest within the end-to-end context of a web request.
    E.g. The hardware device used to make the request or the mobile network that the device is currently using.
    """

    def __init__(self, pipeline):
        """
        FlowData constructor.

        :param pipeline: parent pipeline
        :type pipeline: Pipeline
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
        This can only be run once per flowData instance.

        :return: flowData
        :rtype: FlowData
        """

        if not self.processed:

            for flowElement in self.pipeline.flowElements:
                if self.stopped is not True:
                    # All errors are caught and stored in an errors array keyed by the
                    # flowElement that set the error

                    try:
                        flowElement.process(self)

                    except Exception as inst:

                        key = flowElement.dataKey

                        self.setError(key, str(inst))

            # Set processed flag to true. flowData can only be processed once

            self.processed = True
            return self

        else:
            self.setError("error", "FlowData already processed")

    def getFromElement(self, flowElement):
        """
        Retrieve data by flowElement object.

        :param flowElement: FlowElement that created the data of interest
        :type flowElement: FlowElement
        :return: Data that was created by the flowElement held in the FlowData
        :rtype: ElementData
        """

        try:
            return self.get(flowElement.dataKey)

        except Exception:
            return None

    def get(self, flowElementKey):
        """
        Retrieve data by flowElement key.
        Called by FlowData.getFromElement method.

        :param flowElementKey: FlowElement.dataKey of the FlowElement that created the data of interest
        :type flowElementKey: str
        :return: Data in the FlowData instance that is under the specified key
        :rtype: ElementData
        """

        try:
            return self.data[flowElementKey.lower()]

        except Exception:
            return None

    def __getattr__(self, flowElementKey):
        """
        Magic getter to allow retrieval of data from FlowData.data[flowElementKey] by flowElement name.

        :param flowElementKey: dataKey of the FlowElement that created the data of interest
        :type flowElementKey: str
        :return: Data in the FlowData that is under the specified key
        :rtype: ElementData
        """

        return self.get(flowElementKey)

    def setElementData(self, elData):
        """
        Set data (used by flowElement) within FlowData.data

        :param elData: elementData to be added to flowData
        :type elData: ElementData
        """

        self.data[elData.flowElement.dataKey] = elData

    def setError(self, key, error):
        """
        Set error (should be keyed by flowElement dataKey)

        :param key: a flowElement.dataKey
        :type key: str
        :param error: Error message
        :type error: str
        """

        if key not in self.errors:
            self.errors[key] = list()

        self.errors[key].append(error)

        self.pipeline.log("error", error)

    def getEvidenceDataKey(self):
        """
        Get a list of evidence stored in the flowData, filtered by
        its flowElements' evidenceKeyFilters

        :return: filtered evidence
        :rtype: list
        """
        # TODO: check if required

        requestedEvidence = list()

        for flowElement in self.pipeline.flowElements:
            requestedEvidence = requestedEvidence.extend(flowElement.filterEvidence(self))

        return requestedEvidence

    def stop(self):
        """Stop processing any subsequent flowElements"""

        self.stopped = True

    def getWhere(self, propertyFilter):
        """
        Get data from flowElement based on property meta data

        :param propertyFilter: property (metakey, metavalue) shared by all data of interest
        :type propertyFilter: tuple of (str, mixed)
        :return: dictionary of data created by the flowElement that have the specified meta property
        :rtype: dict
        """

        filteredPropertyDictionary = {}

        for flowElement, propertyDictionary in self.pipeline.getProperties().items():
            properties = propertyDictionary.getFiltered(propertyFilter)

            for dataPropertyKey in properties:
                try:
                    filteredPropertyDictionary[dataPropertyKey] = self.get(flowElement).get(dataPropertyKey)
                # We are ignoring errors in getWhere as properties could be missing on purpose
                # They shouldn't throw an error breaking the whole getWhere.
                except Exception:
                    pass

        return filteredPropertyDictionary
