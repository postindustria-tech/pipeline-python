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

from fiftyone_pipeline_core.dataproperty_dictionary import DataPropertyDictionary
from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter
from fiftyone_pipeline_core.logger import Logger

from fiftyone_pipeline_engines.engine import Engine
from fiftyone_pipeline_engines.basic_dictionary_cache import BasicDictionaryCache
from fiftyone_pipeline_engines.aspectdata_dictionary import AspectDataDictionary

from fiftyone_pipeline_engines.aspectproperty_value import AspectPropertyValue

myLogger = Logger(minLevel="debug")

class UserFlowElement(Engine):
    def __init__(self):

        super(UserFlowElement, self).__init__()

        self.dataKey = "user"

        # Run count so as to test caching
        self.runCount = 0

        self.database = {
            "1": {
                "firstName": "Rodderick",
                "lastName": "Jhones",
                "age"   : 12
            },
            "2": {
                "firstName": "Sally",
                "lastName": "Jones",
                "age": 23
            }
        }

        self.properties = DataPropertyDictionary(self)

        self.properties.addProperty("firstName", {
            "type": "string",
            "description": "The user's first name."
        })
        self.properties.addProperty("lastName", {
            "type": "string",
            "description": "The user's last name."
        })

        self.properties.addProperty("age", {
            "type": "int",
            "description": "The user's age."
        })

        self.properties.addProperty("height", {
            "type": "int",
            "description": "The user's height."
        })

    def processInternal(self, flowData):

        self.runCount += 1

        userID = flowData.evidence.get("userID")

        user = self.database[userID]

        user["aspectPropertyValueTestSuccess"] = AspectPropertyValue(value="This is a value")
        user["aspectPropertyValueTestFail"] = AspectPropertyValue(noValueMessage="Reason for no value")

        data = AspectDataDictionary(self, user)

        flowData.setElementData(data)

    def getEvidenceKeyFilter(self):

        return BasicListEvidenceKeyFilter(["userID"])

class CoreTests(unittest.TestCase):

    def test_aspect_property_has_value(self):

        print("Testing aspect property value hasValue()")
            
        fe = UserFlowElement()

        userPipeline = PipelineBuilder().add(fe).build()

        fd = userPipeline.createFlowData()

        fd.evidence.set("userID", "1")

        fd.process()

        # Test has value
    
        self.assertEqual(fd.user.aspectPropertyValueTestSuccess.hasValue(), True)
        self.assertEqual(fd.user.aspectPropertyValueTestFail.hasValue(), False)

    def test_aspect_property_value(self):

        print("Testing aspect property value")
            
        fe = UserFlowElement()

        userPipeline = PipelineBuilder().add(fe).build()

        fd = userPipeline.createFlowData()

        fd.evidence.set("userID", "1")

        fd.process()
    
        self.assertEqual(fd.user.aspectPropertyValueTestSuccess.value(), "This is a value")

    def test_aspect_property_value_error(self):

        print("Testing aspect property value error")
            
        fe = UserFlowElement()

        userPipeline = PipelineBuilder().add(fe).build()

        fd = userPipeline.createFlowData()

        fd.evidence.set("userID", "1")

        fd.process()

        try: 
            fd.user.aspectPropertyValueTestFail.value()
        except Exception as e:
            error = str(e)

        self.assertEqual(error, "Reason for no value")


    def test_cache(self):

        print("Testing cache")

        fe = UserFlowElement()

        fe.addCache(BasicDictionaryCache())

        userPipeline = PipelineBuilder().add(fe).build()

        fd = userPipeline.createFlowData()

        fd.evidence.set("userID", "2")

        fd.process()

        # This run should be cached

        fd2 = userPipeline.createFlowData()

        fd2.evidence.set("userID", "2")

        fd2.process()

        self.assertEqual(fd.user.lastname, "Jones")

        self.assertEqual(fe.runCount, 1)

        fd3 = userPipeline.createFlowData()

        # New evidence, new cache

        fd3.evidence.set("userID", "1")

        fd3.process()

        self.assertEqual(fe.runCount, 2)

    def test_missing_property_service(self):

        print("Testing missing property service")

        fe = UserFlowElement()
        
        userPipeline = PipelineBuilder().add(fe).build()

        fd = userPipeline.createFlowData()

        fd.evidence.set("userID", "2")

        fd.process()

        try:
            fd.get("user").get("height")
        except Exception as e:
            error = str(e)

        self.assertEqual(error, "Missing property height")
