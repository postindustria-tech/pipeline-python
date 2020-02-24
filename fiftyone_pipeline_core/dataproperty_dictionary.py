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


class DataPropertyDictionary:
    """
    The DataPropertyDictionary stores information about a FlowElement's properties and their metadata. It can be queried to retrieve properties depending on this metadata.
    """

    def __init__(self, flowElement):
        """
        Construct DataPropertyDictionary

        :param flowElement: the FlowElement relating to the properties
        :type flowElement: FlowElement
        """

        self.flowElement = flowElement

        self.contents = {}

    def __iter__(self):
        """
        An iterator to make it possible to loop over a property list

        """

        for x in self.contents.items():
            yield x

    def addProperty(self, propertyKey, metaDataDictionary):
        """
        Add property to the dictionary

        :param propertyKey
        :type propertyKey: str
        :param metaDataDictionary:
        :type metaDataDictionary: dict
        """

        self.contents[propertyKey.lower()] = metaDataDictionary
        self.contents[propertyKey.lower()]["flowElement"] = self.flowElement.dataKey

    def getContents(self):
        """
        Get contents as a Dict

        :return:
        :rtype: dict
        """

        return self.contents

    def getFiltered(self, propertyFilter):
        """
        Get a dictionary of properties filtered by a meta key and meta value
        # TODO: Replace this tuple with two separate params as it's over complicated

        :param propertyFilter: Meta key and metavalue to filter by
        :type propertyFilter: tuple(key, value)
        :return: Dictionary of filtered properties
        :rtype: dict
        """

        filtered = {}

        for key, value in self.getContents().items():
            if propertyFilter[0] in value and value[propertyFilter[0]] == propertyFilter[1]:
                filtered[key] = value

        return filtered
