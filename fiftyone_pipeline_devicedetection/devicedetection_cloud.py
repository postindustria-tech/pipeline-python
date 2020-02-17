from fiftyone_pipeline_engines.engine import Engine
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.dataproperty_dictionary import DataPropertyDictionary
from fiftyone_pipeline_engines.aspectproperty_value import AspectPropertyValue

import json


class DeviceDetectionCloud(Engine):

        def __init__(self):

            super(DeviceDetectionCloud, self).__init__()

            self.dataKey = "device"

        def getProperties(self):

            if hasattr(self, "properties"):
                return self.properties
            else:
                return {}

        def makePropertiesList(self, flowData):

            cloudProperties = flowData.cloud.properties["Products"][self.dataKey]["Properties"]

            # set the FlowElement's properties
            self.properties = DataPropertyDictionary(self)

            for cloudProperty in cloudProperties:
                self.properties.addProperty(cloudProperty["Name"], cloudProperty)
            
        def processInternal(self, flowData):

            cloudData = json.loads(flowData.cloud.cloud)

            cloudProperties = flowData.cloud.properties

            self.makePropertiesList(flowData)

            deviceData = cloudData["device"]

            nullValueReasons = cloudData["nullValueReasons"]

            output = {}

            for key,value in deviceData.items():
                if (self.dataKey + "." + key in nullValueReasons):
                    noValueMessage = nullValueReasons[self.dataKey + "." + key]
                    output[key] = AspectPropertyValue(noValueMessage=noValueMessage)
                else:
                    output[key] = AspectPropertyValue(value=value)
            
            data = ElementDataDictionary(self, output)
            flowData.setElementData(data)
