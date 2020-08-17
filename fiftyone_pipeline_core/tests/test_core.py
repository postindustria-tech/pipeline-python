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

from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder

from classes.testpipeline import TestPipeline
from classes.memorylogger import MemoryLogger
from classes.exampleflowelement1 import ExampleFlowElement1
from classes.exampleflowelement2 import ExampleFlowElement2
from classes.stopflowdata import StopFlowData
from classes.errorflowdata import ErrorFlowData


######################################
# The Tests

class CoreTests(unittest.TestCase):

    # Test logging works
    def testLogger(self):
    
        testPipeline = TestPipeline().pipeline

        loggerMessage = testPipeline.logger.memoryLog[0]["message"]
        self.assertTrue(loggerMessage == "test")
 

    # Test getting evidence
    def testEvidence(self):

        testPipeline = TestPipeline()
        userAgent = testPipeline.flowData.evidence.get("header.user-agent")
        self.assertTrue(userAgent == "test")


    # Test filtering evidence
    def testEvidenceKeyFilter(self):

        testPipeline = TestPipeline()
        nullEvidence = testPipeline.flowData.evidence.get("header.other-evidence")
        self.assertTrue(nullEvidence == None)


    # # Test Getter methods
    def testGet(self):
 
        testPipeline = TestPipeline()
        getValue = testPipeline.flowData.get("example1").get("integer")
        self.assertTrue(getValue == 5)
  

    def testGetWhere(self):

        testPipeline = TestPipeline()
        getValue = len(testPipeline.flowData.getWhere("type", "int"))
        self.assertTrue(getValue == 1)
        

    def testGetFromElement(self):

        testPipeline = TestPipeline()
        getValue = testPipeline.flowData.getFromElement(testPipeline.flowElement1).get("integer")
        self.assertTrue(getValue == 5)


    # # Test check stop FlowData works
    def testStopFlowData(self):
 
        testPipeline = TestPipeline()
        getValue = testPipeline.flowData.get("example2")
        self.assertTrue(getValue == None)
   

    # Test errors are returned
    def testErrors(self):

        testPipeline = TestPipeline()
        getValue = testPipeline.flowData.errors["error"]
        self.assertTrue(getValue is not None)

    # Test aspectPropertyValue wrapper

    def testAPV(self):

        testPipeline = TestPipeline()
        yes = testPipeline.flowData.get("apv").get("yes")

        self.assertTrue(yes.hasValue())
        self.assertTrue(yes.value() == "yes")

        no = testPipeline.flowData.get("apv").get("no")

        self.assertFalse(no.hasValue())
        self.assertTrue(no.noValueMessage == "no")
   