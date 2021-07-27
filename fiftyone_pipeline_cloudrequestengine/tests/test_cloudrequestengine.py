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

import unittest

from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.aspectproperty_value import AspectPropertyValue

from fiftyone_pipeline_cloudrequestengine.cloudrequestengine import CloudRequestEngine
from fiftyone_pipeline_cloudrequestengine.requestclient import RequestClient
from fiftyone_pipeline_cloudrequestengine.constants import Constants
from unittest.mock import Mock
from requests import Response

import os

class TestCloudRequestEngine(unittest.TestCase):
    testResourceKey = "resource_key"
    testEndPoint = "http://testEndPoint/"
    testEnvVarEndPoint = "http://testEnvVarEndPoint/"

    class TestRequestClient(RequestClient):
        def request(self, type, name, originHeader):
            propertiesStr = "accessibleProperties"
            evidenceKeysStr = "evidencekeys"

            switches = {
                propertiesStr: "{\"Products\":{\"device\":{\"DataTier\":\"CloudV4Free\",\"Properties\":[{\"Name\":\"IsMobile\",\"Type\":\"Boolean\",\"Category\":\"Device\",\"DelayExecution\":false},{\"Name\":\"JavascriptHardwareProfile\",\"Type\":\"JavaScript\",\"Category\":\"Javascript\",\"DelayExecution\":false}]}}}",
                evidenceKeysStr: "[\"fiftyone.resource-key\"]"
            }
            response = Mock(spec=Response)
            response.status_code = 200
            if propertiesStr in name:
                response.text = switches.get(propertiesStr)
            elif evidenceKeysStr in name:
                response.text = switches.get(evidenceKeysStr)

            return response               


    def setUp(self):
        if os.environ.get(Constants.FOD_CLOUD_API_URL) != None:
            del os.environ[Constants.FOD_CLOUD_API_URL]


    # Check that the explicitly setting the cloud endpoint via method interface
    # take precedence over everything else
    def testConfigEndPoint_ExplicitSetting(self):
        httpClient = self.TestRequestClient()

        os.environ[Constants.FOD_CLOUD_API_URL] = TestCloudRequestEngine.testEnvVarEndPoint
        cloudRequestEngine = CloudRequestEngine({
            "resource_key": TestCloudRequestEngine.testResourceKey,
            "cloud_endpoint": TestCloudRequestEngine.testEndPoint,
            "http_client": httpClient
        })
        self.assertEqual(TestCloudRequestEngine.testEndPoint, cloudRequestEngine.baseURL)


    # Check that the setting the cloud endpoint via environment variable take
    # precedence over the default value
    def testConfigEndPoint_EnvironmentVariableSetting(self):
        httpClient = self.TestRequestClient()

        os.environ[Constants.FOD_CLOUD_API_URL] = TestCloudRequestEngine.testEnvVarEndPoint
        cloudRequestEngine = CloudRequestEngine({
            "resource_key": TestCloudRequestEngine.testResourceKey,
            "http_client": httpClient
        })
        self.assertEqual(TestCloudRequestEngine.testEnvVarEndPoint, cloudRequestEngine.baseURL)


    # Check that if nothing else is set the default value should be used
    def testConfigEndPoint_DefaultSetting(self):
        httpClient = self.TestRequestClient()

        cloudRequestEngine = CloudRequestEngine({
            "resource_key": TestCloudRequestEngine.testResourceKey,
            "http_client": httpClient
        })
        self.assertEqual(Constants.BASE_URL_DEFAULT, cloudRequestEngine.baseURL)
