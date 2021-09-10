 # *********************************************************************
 # This Original Work is copyright of 51 Degrees Mobile Experts Limited\
 # Copyright 2019 51 Degrees Mobile Experts Limited, 5 Charlotte Close,
 # Caversham, Reading, Berkshire, United Kingdom RG4 7BY\
 #
 # This Original Work is licensed under the European Union Public Licence (EUPL) 
 # v\1\2 and is subject to its terms as set out below\
 #
 # If a copy of the EUPL was not distributed with this file, You can obtain
 # one at https://opensource\org/licenses/EUPL-1\2\
 #
 # The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
 # amended by the European Commission) shall be deemed incompatible for
 # the purposes of the Work and the provisions of the compatibility
 # clause in Article 5 of the EUPL shall not apply\
 # 
 # If using the Work as, or as part of, a network application, by 
 # including the attribution notice(s) required under Article 5 of the EUPL
 # in the end user terms of the application under an appropriate heading, 
 # such notice(s) shall fulfill the requirements of that article\
 # ********************************************************************

from classes.cloudrequestengine_testbase import CloudRequestEngineTestsBase
from fiftyone_pipeline_cloudrequestengine.cloudrequestengine import CloudRequestEngine
from fiftyone_pipeline_cloudrequestengine.cloudrequestexception import CloudRequestException
from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder
from classes.constants import *
import json
import unittest

class TestCloudResponse(CloudRequestEngineTestsBase):

    def test_process(self):
    
        """
            Test cloud request engine adds correct information to post request
            and returns the response in the ElementData
        """
        
        httpClient = self.mock_http()
        
        engine = CloudRequestEngine({"resource_key": Constants.resourceKey,
            "http_client" : httpClient})

        builder= PipelineBuilder();
        pipeline = builder.add(engine).build()

        data = pipeline.create_flowdata()
        data.evidence.add("query.User-Agent", Constants.userAgent)

        data.process()

        result = data.get_from_element(engine)["cloud"]

        self.assertEqual(Constants.jsonResponse, result)

        jsonObj = json.loads(result)
        self.assertEqual(1, jsonObj["device"]["value"])

    def test_sub_properties(self):
        
        """
            Verify that the CloudRequestEngine can correctly parse a
            response from the accessible properties endpoint that contains
            meta-data for sub-properties.
        """

        httpClient = self.mock_http()

        engine = CloudRequestEngine({
            "resource_key" : "subpropertieskey",
            "http_client" : httpClient
        })

        self.assertEqual(2, len(engine.flow_element_properties))     
        deviceProperties = engine.flow_element_properties["device"]
        self.assertEqual(2, len(deviceProperties));
        self.assertTrue(self.properties_contain_name(deviceProperties, "IsMobile"));
        self.assertTrue(self.properties_contain_name(deviceProperties, "IsTablet"));
        devicesProperties = engine.flow_element_properties["devices"]
        self.assertFalse(devicesProperties is None)
        self.assertEqual(1, len(devicesProperties))
        self.assertTrue(self.properties_contain_name(devicesProperties["Devices"]["itemproperties"], "IsMobile"))
        self.assertTrue(self.properties_contain_name(devicesProperties["Devices"]["itemproperties"], "IsTablet"))

    def test_validate_error_handling_invalid_resourceKey(self):
    
        """ 
            Test cloud request engine handles errors from the cloud service 
            as expected.
            An exception should be thrown by the cloud request engine
            containing the errors from the cloud service when resource key
            is invalid.
        """ 

        httpClient = self.mock_http()

        exception = None

        try:
            engine = CloudRequestEngine({
                "resource_key" : Constants.invalidKey,
                "http_client" : httpClient
            })
        except CloudRequestException as ex:
            exception = ex

        self.assertIsNotNone("Expected exception to occur", exception)
        self.assertEqual(str(exception), Constants.invalidKeyMessageComplete)

    def test_validate_error_handling_nodata(self):
        
        """ 
            Test cloud request engine handles a lack of data from the 
            cloud service as expected.
            An exception should be thrown by the cloud request engine.
        """ 

        httpClient = self.mock_http()

        exception = None

        try:
            engine = CloudRequestEngine({
                "resource_key" : Constants.noDataKey,
                "http_client" : httpClient
            })
        except CloudRequestException as ex:
            exception = ex

        self.assertIsNotNone("Expected exception to occur", exception)
        self.assertEqual(str(exception), Constants.noDataKeyMessageComplete)

    def test_validate_error_handling_noerror_nosuccess(self):
        
        """ 
            Test cloud request engine handles no success error from the 
            cloud service as expected.
            An exception should be thrown by the cloud request engine.
        """ 

        httpClient = self.mock_http()

        exception = None

        try:
            engine = CloudRequestEngine({
                "resource_key" : Constants.noErrorNoSuccessKey,
                "http_client" : httpClient
            })
        except CloudRequestException as ex:
            exception = ex

        self.assertIsNotNone("Expected exception to occur", exception)
        self.assertEqual(str(exception), Constants.noErrorNoSuccessMessage)
