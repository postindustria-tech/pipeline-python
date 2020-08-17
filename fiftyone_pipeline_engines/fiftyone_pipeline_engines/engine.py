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

from fiftyone_pipeline_core.flowelement import FlowElement

import json

class Engine(FlowElement):

    def __init__(self):

        super(Engine, self).__init__()
    
    def setCache(self, cache):
        """
        Add a cache to an engine
        @type casee: Cache
        @param cache: Cache with get and set methods

        """
        
        self.cache = cache


    def setRestrictedProperties(self, propertiesList):
        """"
        Add a subset of properties
        
        @type propertiesList: string[] 
        @param propertiesList: An array of properties to include
        
        """
 
        self.restrictedProperties = propertiesList
  

    def inCache(self, flowData):
        """
        A method to check if a flowData's evidence is in the cache
        
        @type FlowData: FlowData
        @param FlowData:

        @rtype: bool
        @return: True or false: a flowData's evidence is in the cache

        """
    
        keys = self.filterEvidence(flowData)

        cacheKey = json.dumps(keys)

        cached = self.cache.getCacheValue(cacheKey)

        if cached is not None:
            flowData.setElementData(cached)

            return True
        else:
            return False
  



    def process(self, flowData):

        """
        Engine's core process function.
        Calls specific overriden processInternal methods but wraps it in a cache check
        and a cache put
        
        @type lowData: FlowData
        @param flowData:
        
        """

        if hasattr(self, "cache"):

            if self.inCache(flowData):
                return True
            else:
                self.processInternal(flowData)
                cacheKey = json.dumps(self.filterEvidence(flowData))
                self.cache.setCacheValue(cacheKey, flowData.get(self.dataKey))

        else:

            self.processInternal(flowData)
