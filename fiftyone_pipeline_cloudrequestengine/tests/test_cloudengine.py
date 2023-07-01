# *********************************************************************
# This Original Work is copyright of 51 Degrees Mobile Experts Limited.
# Copyright 2023 51 Degrees Mobile Experts Limited, Davidson House,
# Forbury Square, Reading, Berkshire, United Kingdom RG1 3EU.
#
# This Original Work is licensed under the European Union Public Licence
# (EUPL) v.1.2 and is subject to its terms as set out below.
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
# ********************************************************************* 

from fiftyone_pipeline_cloudrequestengine.cloudrequestengine import CloudRequestEngine
from fiftyone_pipeline_cloudrequestengine.cloudrequestexception import CloudRequestException
from fiftyone_pipeline_cloudrequestengine.cloudengine import CloudEngine
from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder
from urllib.parse import urlencode
import unittest
import json
import os

if "resource_key" in os.environ:
    resource_key = os.environ["resource_key"]
else:
    resource_key = "!!YOUR_RESOURCE_KEY!!"

class CloudEngineTests(unittest.TestCase):

    def test_cloud_engine(self):

        """!
        Verify that cloud engine returns isMobile property in response.
        This is an integration test that uses the live cloud service
        so any problems with that service could affect the result
        of this test.
        """

        if (resource_key == "!!YOUR_RESOURCE_KEY!!"):
            self.assertFalse("""You need to create a resource key at 
            https://configure.51degrees.com and paste it into the
            code, replacing !!YOUR_RESOURCE_KEY!!. Please make sure
            to include IsMobile property.""")

        cloud = CloudRequestEngine({"resource_key" : resource_key})

        engine = CloudEngine()

        engine.datakey = "device"

        pipeline = PipelineBuilder()

        pipeline = pipeline.add(cloud).add(engine).build()

        fd = pipeline.create_flowdata()

        fd.evidence.add("header.user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")

        result = fd.process()

        self.assertTrue(result.device.ismobile.has_value())


    def test_cloud_post_request_with_sequence_evidence(self):

        """!
        Verify that making POST request with SequenceElement evidence
        will not return any errors from cloud.
        This is an integration test that uses the live cloud service
        so any problems with that service could affect the result
        of this test.
        """

        if (resource_key == "!!YOUR_RESOURCE_KEY!!"):
            self.assertFalse("""You need to create a resource key at 
            https://configure.51degrees.com and paste it into the
            code, replacing !!YOUR_RESOURCE_KEY!!. Please make sure
            to include IsMobile property.""")

        cloud = CloudRequestEngine({"resource_key" : resource_key})

        engine = CloudEngine()

        engine.datakey = "device"

        pipeline = PipelineBuilder()

        pipeline = pipeline.add(cloud).add(engine).build()

        fd = pipeline.create_flowdata()

        fd.evidence.add("query.session-id", "8b5461ac-68fc-4b18-a660-7bd463b2537a")
        fd.evidence.add("query.sequence", 1)

        result = fd.process()
        self.assertTrue(len(result.errors) == 0)

    def test_cloud_get_request_with_sequence_evidence(self):

        """!
        Verify that making GET request with SequenceElement evidence
        in query params will return an error from cloud 
        This is an integration test that uses the live cloud service
        so any problems with that service could affect the result
        of this test.
        """

        if (resource_key == "!!YOUR_RESOURCE_KEY!!"):
            self.assertFalse("""You need to create a resource key at 
            https://configure.51degrees.com and paste it into the
            code, replacing !!YOUR_RESOURCE_KEY!!. Please make sure
            to include IsMobile property.""")

        cloud = CloudRequestEngine({"resource_key" : resource_key})

        engine = CloudEngine()

        engine.datakey = "device"

        pipeline = PipelineBuilder()

        pipeline = pipeline.add(cloud).add(engine).build()

        fd = pipeline.create_flowdata()

        fd.evidence.add("query.session-id", "8b5461ac-68fc-4b18-a660-7bd463b2537a")
        fd.evidence.add("query.sequence", 1)

        url = cloud.baseURL + cloud.resource_key + ".json?"

        evidence = fd.evidence.get_all()

        # Remove prefix from evidence

        evidenceWithoutPrefix = {}

        for key, value in evidence.items():       
            keySplit =  key.split('.')
            try:
                keySplit[1]
            except:
                continue
            else:
                evidenceWithoutPrefix[keySplit[1]] = value
        url += urlencode(evidenceWithoutPrefix)
        
        # Following try catch block should be removed once error
        # is fixed in cloud
        try:
            cloud.make_cloud_request('GET', url, content=None)
        except Exception as ex:
            self.assertTrue("Sequence number not present in evidence. this is mandatory" in str(ex))

        # Following statements should be uncommented once error
        # is fixed in cloud
        # jsonResponse = cloud.make_cloud_request('GET', url, content=None)
        # self.assertTrue(len(jsonResponse["errors"]) == 0)

    def test_HttpDataSetInException(self):
    
        """!
        Check that errors from the cloud service will cause the
        appropriate data to be set in the CloudRequestException.
        """

        resource_key = "resource_key"
        
        pipeline = PipelineBuilder()

        try:
            cloud = CloudRequestEngine({"resource_key" : resource_key})       
            pipeline = pipeline.add(cloud).build()
            self.assertFalse("Expected exception did not occur")
        except CloudRequestException as ex:
            self.assertTrue(ex.httpStatusCode > 0, "Status code should not be 0")
            self.assertIsNotNone(ex.responseHeaders, "Response headers not populated")
            self.assertTrue(len(ex.responseHeaders) > 0, "Response headers not populated")