from fiftyone_pipeline_engines.engine import Engine
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.dataproperty_dictionary import DataPropertyDictionary

import requests

class CloudRequestEngine(Engine):

        def __init__(self, resourceKey, baseURL = "https://cloud.51degrees.com/api/v4/"):

            super(CloudRequestEngine, self).__init__()

            self.dataKey = "cloud"
            self.resourceKey = resourceKey
            self.baseURL = baseURL

        # Get the available properties for all cloud products attached to resource key
        def getCloudProperties(self):

            properties = {}

            propertiesURL = self.baseURL + "accessibleProperties?resource=" + self.resourceKey

            cloudRequest = requests.get(propertiesURL)

            if cloudRequest.status_code == 200:
                properties = cloudRequest.json()
            else:
                raise Exception("CloudRequestEngine error " + str(cloudRequest.status_code))

            return properties

        def processInternal(self, flowData):

            properties = self.getCloudProperties()

            url = self.baseURL + self.resourceKey + ".json?"

            evidence = flowData.evidence.getAll()

            queryString = {}

            for key, value in evidence.items():
                if "." in key:
                    key = key.split(".")[1]
                
                queryString[key] = value


            cloudRequest = requests.get(url, queryString)

            if cloudRequest.status_code == 200:
                data = ElementDataDictionary(self, {"cloud" : cloudRequest.text, "properties": properties})
                flowData.setElementData(data)
            else:
                raise Exception("CloudRequestEngine error " + str(cloudRequest.status_code))

