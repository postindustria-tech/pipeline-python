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


class ElementData(object):
    """Core ElementData class
    # ElementData is where FlowElements store data (following processing via a FlowData and Pipeline)
    # How that data is stored and retrieved is up to the ElementData class extension

    """

    def __init__(self, flowElement):
        """Constructor for ElementData""
        :param flowElement: FlowElement that data has been created by
        :type flowElement: FlowElement
        """

        self.flowElement = flowElement

    def get(self, key):
        """
        Get a value from the elementData contents
        Proxy for the ElementData.getInternal method

        :param key: property
        :type key: str
        :return: specified property from the data
        :rtype: mixed
        """

        return self.getInternal(key.lower())

    def __getattr__(self, key):
        """
        Magic getter for a property from the data
        Allowing  user to write for example Data.IsMobile rather than Data.get("IsMobile)

        :param key: property
        :type key: str
        :return: specified property from the data
        :rtype: mixed
        """

        return self.get(key)

    def getInternal(self, key):
        """
        Returns the requested property from the data
        Overridden by specific ElementData instances.

        :param key: property
        :type key: str
        :return: requested property from data
        :rtype: mixed
        """

        return

    def getProperties(self):
        """
        Proxy to the data's flowElement properties.
        Gets the FlowElement.properties of the parent FlowElement.

        :return: dictionary of the parent FlowElement's properties
        :rtype: DataPropertyDictionary
        """

        return self.flowElement.getProperties()
