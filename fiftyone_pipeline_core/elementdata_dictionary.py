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

from .elementdata import ElementData


class ElementDataDictionary(ElementData):
    """
    `ElementData`:class: class extension that stores content as dictionary
    """

    def __init__(self, flowElement, contents):
        """
        Constructor for Element Data Dictionary

        :param flowElement: `FlowElement` that creates the data to be stored
        :type flowElement: `FlowElement`:class: instance
        :param contents: dictionary contents
        :type contents: mixed dict
        # TODO: contents type originally noted as "mixed[]" ?
        """

        # TODO: Does this need a superclass call?

        self.contents = {}

        for key, value in contents.items():
            self.contents[key.lower()] = value

        self.flowElement = flowElement

        ElementData(flowElement)

    def asDictionary(self):
        """"
        Get the values contained in the elementData instance as a dictionary
        of keys and values.

        :returns: a dictionary of mixed[]
        """
        return self.contents

    def getInternal(self, key):
        """
        getInternal - Internal getter for contents
        param: string key
        returns: mixed
        """

        if (key in self.contents):

            return self.contents[key]

        else:

            return
