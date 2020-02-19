import unittest

from fiftyone_pipeline_core.dataproperty_dictionary import DataPropertyDictionary
from fiftyone_pipeline_engines.aspectproperty_value import AspectPropertyValue
from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder
from fiftyone_pipeline_engines.engine import Engine
from fiftyone_pipeline_cloudrequestengine.cloudrequest_engine import CloudRequestEngine
from fiftyone_pipeline_devicedetection.devicedetection_cloud import DeviceDetectionCloud

cre = CloudRequestEngine("AQS5HKcyHJbECm6E10g")
ddCloud = DeviceDetectionCloud()

myPipeline = PipelineBuilder().add(cre).add(ddCloud).build()

class CoreTests(unittest.TestCase):

    def test_properties(self):

        print("Testing propertylist")
            
        fd = myPipeline.createFlowData()

        fd.evidence.set("header.user-agent", "Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10")

        fd.process()

        for dataPropertyKey, dataPropertyValue in fd.device.getProperties():
            print(dataPropertyKey, dataPropertyValue)
            self.assertEqual("Name" in dataPropertyValue, True)

    def test_user_agent_good(self):

        print("Testing phone user agent")
            
        fd = myPipeline.createFlowData()

        fd.evidence.set("header.user-agent", "Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10")

        fd.process()

        self.assertEqual(fd.device.ismobile.hasValue(), True)
        self.assertEqual(fd.device.ismobile.value(), True)

    def test_user_agent_bad(self):

        print("Testing bad user agent")
            
        fd = myPipeline.createFlowData()

        fd.evidence.set("header.user-agent", "Bad")

        fd.process()

        self.assertEqual(fd.device.ismobile.hasValue(), False)
        
        try:
            fd.device.ismobile.value()
        except Exception as e:
            error = str(e)

        self.assertEqual(type(error), str)





    

