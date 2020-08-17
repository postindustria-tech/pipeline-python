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


"""
    The JSONBundler aggregates all properties from FlowElements into a JSON object
    It is used for retrieving via an endpoint from the client
    side via the JavaScriptBuilder and also used inside the
    JavaScriptBuilder itself to pass properties to the client side.
    Both this and the JavaScriptBuilder element are automatically
    added to a Pipeline unless specifically ommited in the PipelineBuilder

"""

from .flowelement import FlowElement
from .elementdata_dictionary import ElementDataDictionary

class JSONBundlerElement(FlowElement):

    def __init__(self):

        super(JSONBundlerElement, self).__init__()

        self.dataKey = "jsonbundler"

        self.properties = {"json" : { "type": "dict"} }

        self.propertyCache = {}

    """
    The JSONBundler extracts all properties from a FlowData and serializes them into JSON
    @type FlowData:
    @param FlowData: A FlowData
    
    """
    def processInternal(self, flowData):
   
        # Get every property on every FlowElement
        # Storing JavaScript properties in an extra section

        output = {"javascriptProperties": [] }

        if len(self.propertyCache):
            propertyCacheSet = True
        else:
            propertyCacheSet = False
        
        for flowElement in flowData.pipeline.flowElements:

            if flowElement.dataKey == "jsonbundler" or flowElement.dataKey == "sequence" or flowElement.dataKey == "javascriptbuilder":
                continue
            
            properties = flowElement.getProperties()

            if not propertyCacheSet:

                delayExecutionList = []
                delayedEvidenceProperties = {}

                # Loop over all properties and see if any have delay execution set to true

                for propertyKey, propertyMeta in properties.items():
                    
                    if "delayexecution" in propertyMeta and propertyMeta["delayexecution"] == True:
                        delayExecutionList.append(propertyKey)

                
                """
                Loop over all properties again and see if any have evidenceproperties which
                have delayedExecution set to true
                """

                for propertyKey, propertyMeta in properties.items():

                    if("evidenceproperties" in propertyMeta):

                        delayedEvidencePropertiesList = list(filter(lambda x: x in delayExecutionList, propertyMeta["evidenceproperties"]))

                        if len(delayedEvidencePropertiesList):
                            
                            delayedEvidenceProperties[propertyKey] = list(map(lambda x:
                                flowElement.dataKey + '.' + x, delayedEvidencePropertiesList))


                self.propertyCache[flowElement.dataKey] = {
                    "delayExecutionList": delayExecutionList,
                    "evidenceProperties": delayedEvidenceProperties
                }

            propertyCache = self.propertyCache[flowElement.dataKey]

            # Create empty area for FlowElement properties to go

            output[flowElement.dataKey] = {}

            for propertyKey, propertyMeta in properties.items():
                value = None
                nullReason = "Unknown"

                # Check if property has delayed execution and set in JSON if yes


                if propertyKey in propertyCache["delayExecutionList"]:
                    output[flowElement.dataKey][propertyKey.lower() + "delayexecution"] = True
                

                # Check if property has any delayed execution evidence properties and set in JSON if yes

                if propertyKey in propertyCache["evidenceProperties"]:
                    output[flowElement.dataKey][propertyKey.lower() + 'evidenceproperties'] = propertyCache["evidenceProperties"][propertyKey]
                

                try:

                    valueContainer = flowData.get(flowElement.dataKey).get(propertyKey)

                    # Check if value is of the aspect property value type

                    if isinstance(valueContainer, object) and hasattr(valueContainer, "hasValue" ):
                    
                        # Check if it has a value

                        if valueContainer.hasValue():
                            value = valueContainer.value()
                        else:
                            value = None
                            nullReason = valueContainer.noValueMessage
                        
                    # Check if list of aspect property values

                    elif isinstance(valueContainer, list) and isinstance(valueContainer[0], object):

                        output = []

                        for item in valueContainer:
                            if item.hasValue():
                                output.append(item.value())
                            else:
                                nullReason = item.noValueMessage

                        value = output

                    else:

                        # Standard value
                        value = valueContainer
                    
                except:
                    # Catching missing property exceptions and other errors

                    continue
               

                output[flowElement.dataKey.lower()][propertyKey.lower()] = value
                if value is None:
                   output[flowElement.dataKey.lower()][propertyKey.lower() + "nullreason"] = nullReason

                sequence = flowData.evidence.get("query.sequence")

                if sequence is None or sequence < 10: 

                    if "type" in propertyMeta and propertyMeta["type"].lower() == "javascript":

                        output["javascriptProperties"].append(flowElement.dataKey.lower() + "." + propertyKey.lower())
                 

        data = ElementDataDictionary(self, {"json": output})

        flowData.setElementData(data)

        return
