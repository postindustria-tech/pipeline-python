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

from fiftyone_pipeline_core.elementdata import ElementData
from fiftyone_pipeline_core.logger import Logger


class AspectData(ElementData):
    """
    * AspectData extends elementData by adding the option of a missing property service
    * It also allows properties to be explicitly excluded by a flowElement / engine
    """

    def missingPropertyService(self, missingPropertyKey, missingPropertyMeta):

        raise Exception("Missing property " + missingPropertyKey)

    def get(self, key):
        """
        * get - Get a value (unless in a flowElement's restrictedProperties list)
        * If property not found, call the attached missing property service
        * param: string key
        * returns: mixed
        """

        result = self.getInternal(key.lower())

        if result is None:
            properties = self.flowElement.getProperties().getContents()
            if key in properties:
                self.missingPropertyService(key, properties[key])
        else:
            return result
    