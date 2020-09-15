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
import json

from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter
from fiftyone_pipeline_core.logger import Logger
from fiftyone_pipeline_core.aspectproperty_value import AspectPropertyValue

from fiftyone_pipeline_engines.engine import Engine
from fiftyone_pipeline_engines.datakeyed_cache import DataKeyedCache
from fiftyone_pipeline_engines.aspectdata_dictionary import AspectDataDictionary

class TestCache(DataKeyedCache):
    
    def __init__(self):

        self.cache = {}
        self.cacheHits = 0

    def get_cache_value(self, key):
        if key in self.cache:
            self.cacheHits += 1
            return self.cache[key]
        else:
            return None

    def set_cache_value(self, key, value):
        self.cache[key] = value

class ExampleAspectEngine(Engine):

    def __init__(self):

        super(ExampleAspectEngine, self).__init__()

        self.datakey = "example"

        self.properties = {
            "integer": {
                "type" : "int"
            },
            "boolean": {
                "type" : "bool"
            }
        }

    def get_evidence_key_filter(self):

        return BasicListEvidenceKeyFilter(["header.test"])
        
    def process_internal(self, flowData):

        data = AspectDataDictionary(self, {"integer" : 5, "boolean" : True})

        flowData.set_element_data(data)

class EngineTests(unittest.TestCase):

    # Test Engine processing
    def testEngineProcessing(self):
    
        testPipeline = PipelineBuilder().add(ExampleAspectEngine()).build()

        flowData = testPipeline.create_flowdata()

        flowData.process()

        self.assertTrue(flowData.example.integer == 5)

    # Test restricting properties
    def testRestrictedProperty(self):
        
        engine = ExampleAspectEngine()

        engine.set_restricted_properties(["boolean"])

        testPipeline = PipelineBuilder().add(engine).build()

        flowData = testPipeline.create_flowdata()

        flowData.process()

        try:
            flowData.example.get("integer")
        except Exception as e:
            result = str(e)

        self.assertTrue(result == "Property integer was excluded from example")

    # Test restricting properties
    def testMissingPropertyService(self):
        
        engine = ExampleAspectEngine()

        testPipeline = PipelineBuilder().add(engine).build()

        flowData = testPipeline.create_flowdata()

        flowData.process()

        try:
           flowData.example.get("missing")
        except Exception as e:
            result = str(e)

        self.assertTrue(result == "Property missing not found in example")

    # Test cache
    
    def testCache(self):
        
        engine = ExampleAspectEngine()

        cache = TestCache()

        engine.set_cache(cache)

        testPipeline = PipelineBuilder().add(engine).build()

        flowData = testPipeline.create_flowdata()

        flowData.evidence.add("header.test", "test")

        flowData.process()

        flowData2 = testPipeline.create_flowdata()

        flowData2.evidence.add("header.test", "test")

        flowData2.process()

        self.assertEqual(cache.cacheHits, 1)
