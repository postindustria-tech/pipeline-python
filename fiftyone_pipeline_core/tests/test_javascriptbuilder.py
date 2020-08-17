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


class TestEngine(FlowElement):

    def __init__(self):

        super(TestEngine, self).__init__()

        self.dataKey = "test"

        self.properties = { 
            "javascript" : {
                "type" : "javascript"
            },
            "apvGood" : {
                "type" : "string"
            },
            "apvBad" : {
                "type" : "string"
            },
            "normal" : {
                "type" : "boolean"
            }
        }


    def processInternal(self, FlowData):
 
        contents = {}

        contents["javascript"] = "console.log('hello world')"
        contents["normal"] = True

        contents["apvGood"] = AspectPropertyValue(None, "Value")
        contents["apvBad"] =  AspectPropertyValue("No value")

        data =  ElementDataDictionary(self, contents)

        FlowData.setElementData(data)


class TestPipeline():

    def __init__(self, minify = None):
  
        if minify == None:
            pipelineSettings = {}
        else:
            jsSettings = {'minify' : minify}
            pipelineSettings = {'javascriptBuilderSettings' : jsSettings}
        
        self.Pipeline = PipelineBuilder(pipelineSettings)\
            .add(TestEngine())\
            .build()


class DelayedExecutionEngine1(FlowElement):

    def __init__(self):

        super(DelayedExecutionEngine1, self).__init__()

        self.dataKey = "delayedexecutiontest1"

        self.properties = {
            "one" : {
                "delayexecution" : False,
                "type" : 'javascript'
            },
            "two" : {
                "evidenceproperties" : ['jsontestengine']
            }
        }

    def processInternal(self, flowData):

        contents = {
            "one" : 1,
            "two" : 2
        }

        data = ElementDataDictionary(self, contents)

        flowData.setElementData(data)


class DelayedExecutionEngine2(FlowElement):

    def __init__(self):

        super(DelayedExecutionEngine2, self).__init__()

        self.dataKey = "delayedexecutiontest2"
            
        self.properties = {
            "one" : {
                "delayexecution" : True,
                "type" : 'javascript'
            },
            "two" : {
                "evidenceproperties" : ['one']
            }
        }

    def processInternal(self, flowData):


        contents = {
            "one" : 1,
            "two" : 2
        }

        data =  ElementDataDictionary(self, contents)

        flowData.setElementData(data)


class DelayedExecutionEngine3(FlowElement):

    def __init__(self):

        super(DelayedExecutionEngine3, self).__init__()

        self.dataKey = "delayedexecutiontest3"
  
        self.properties = {
            "one" : {
                "evidenceproperties" : ['two', 'three']
            },
            "two" : {
                "delayexecution" : True
            },
            "three" : {
                "delayexecution" : False
            }
        }

    def processInternal(self, flowData):


        contents = {
            "one" : 1,
            "two" : 2,
            "three" : 3
        }

        data = ElementDataDictionary(self, contents)

        flowData.setElementData(data)



class JavaScriptBundlerTests(unittest.TestCase):

    def testJSONBundler(self):
    
        Pipeline = TestPipeline(False).Pipeline

        FlowData = Pipeline.createFlowData()

        FlowData.process()

        expected = {
            'javascriptProperties' :
            [
              'test.javascript',
            ],
            'test' :
            {
                'javascript' : 'console.log(\'hello world\')',
                'apvgood' : 'Value',
                'apvbad' : None,
                'apvbadnullreason' : 'No value',
                'normal' : True,
            }
        }

        self.assertEqual(FlowData.jsonbundler.json, expected)
 

    def testJavaScriptBuilder_Minify(self):
   
        # Generate minified javascript
        Pipeline = (TestPipeline(True)).Pipeline
        FlowData = Pipeline.createFlowData()
        FlowData.process()
        minified = FlowData.javascriptbuilder.javascript

        # Generate non-minified javascript
        Pipeline = (TestPipeline(False)).Pipeline
        FlowData = Pipeline.createFlowData()
        FlowData.process()
        nonminified = FlowData.javascriptbuilder.javascript

        # Generate javascript with default settings
        Pipeline = (TestPipeline()).Pipeline
        FlowData = Pipeline.createFlowData()
        FlowData.process()
        default = FlowData.javascriptbuilder.javascript

        # We don't want to get too specific here. Just check that 
        # the minified version is smaller to confirm that it's
        # done something.

        self.assertTrue(len(minified) < len(nonminified))

        # Check that default is to minify the output
        self.assertTrue(len(default) < len(nonminified))


    def testSequence(self):

        Pipeline = ( TestPipeline(False)).Pipeline

        FlowData = Pipeline.createFlowData()

        FlowData.evidence.set("query.session-id", "test")
        FlowData.evidence.set("query.sequence", 10)

        FlowData.process()

        self.assertEqual(FlowData.evidence.get("query.sequence"), 11)

        self.assertEqual(len(FlowData.jsonbundler.json["javascriptProperties"]), 0)


    def test_jsonbundler_when_delayed_execution_false(self):
 
        pipeline = PipelineBuilder()

        pipeline.add(DelayedExecutionEngine1())
        pipeline = pipeline.build()

        flowData = pipeline.createFlowData()

        flowData.process()

        expected = {"one" : 1, "two" : 2}
        actual = flowData.jsonbundler.json["delayedexecutiontest1"]
        self.assertEqual(actual, expected)



    def test_jsonbundler_when_delayed_execution_true(self):

        pipeline = PipelineBuilder()

        pipeline.add(DelayedExecutionEngine2())
        pipeline = pipeline.build()

        flowData = pipeline.createFlowData()

        flowData.process()

        expected = {
            "onedelayexecution" : True,
            "one" : 1,
            "twoevidenceproperties" :  ['delayedexecutiontest2.one'],
            "two" : 2
        }

        actual = flowData.jsonbundler.json["delayedexecutiontest2"]
        self.assertEqual(actual, expected)



    def test_jsonbundler_when_delayed_execution_multiple(self):

        pipeline = PipelineBuilder()

        pipeline.add(DelayedExecutionEngine3())
        pipeline = pipeline.build()

        flowData = pipeline.createFlowData()

        flowData.process()

        expected = {
            "oneevidenceproperties" : ['delayedexecutiontest3.two'],
            "one" : 1,
            "twodelayexecution": True,
            "two" : 2,
            "three" : 3
        }

        actual = flowData.jsonbundler.json["delayedexecutiontest3"]
        self.assertEqual(actual, expected)
