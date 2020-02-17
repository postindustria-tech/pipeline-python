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
from fiftyone_pipeline_javascriptbundler.javascriptbundler import JavascriptBundler
from fiftyone_pipeline_engines.aspectproperty_value import AspectPropertyValue

class JSFlowElement1(FlowElement):
    def __init__(self):

        super(JSFlowElement1, self).__init__()

        self.dataKey = "js1"


        self.properties = DataPropertyDictionary(self)

        self.properties.addProperty("getBrowserWidth", {
            "type": "javascript",
            "description": "Get width of browser window."
        })


    def processInternal(self, flowData):

        data = ElementDataDictionary(self, {"getBrowserWidth" : "alert(window.innerWidth);"})

        flowData.setElementData(data)



class JSFlowElement2(FlowElement):
    def __init__(self):

        super(JSFlowElement2, self).__init__()

        self.dataKey = "js2"

        self.properties = DataPropertyDictionary(self)

        self.properties.addProperty("getBrowser-Height", {
            "type": "javascript",
            "description": "Get height of browser window."
        })


    def processInternal(self, flowData):

        browserHeight = AspectPropertyValue(value="alert(window.innerHeight)")

        data = ElementDataDictionary(self, {"getBrowser-Height" : browserHeight})

        flowData.setElementData(data)


class NoJSFlowElement(FlowElement):
    
    def __init__(self):

        super(NoJSFlowElement, self).__init__()

        self.dataKey = "nojs"

        self.properties = DataPropertyDictionary(self)

        self.properties.addProperty("other", {
            "type": "string",
            "description": "Dummy, non javascript property."
        })


    def processInternal(self, flowData):

        data = ElementDataDictionary(self, {"other" : "no javascript here"})

        flowData.setElementData(data)


class CoreTests(unittest.TestCase):

    def test_javascript_bundler_one_property(self):

        print("Testing JavaScript bundler with one property")
            
        myPipleine = PipelineBuilder().add(JSFlowElement1()).add(JavascriptBundler()).build()

        fd = myPipleine.createFlowData()

        fd.process()

        desired = "let FOD_CO = class { constructor(){};getbrowserwidth = function(){alert(window.innerWidth);}; }; var fod_co = new FOD_CO(); fod_co.getbrowserwidth();"

        self.assertEqual(fd.javascript.javascript.strip(), desired.strip())

    def test_javascript_bundler_two_properties(self):

        print("Testing JavaScript bundler with two properties")
            
        myPipleine = PipelineBuilder().add(JSFlowElement1()).add(JSFlowElement2()).add(JavascriptBundler()).build()

        fd = myPipleine.createFlowData()

        fd.process()

        desired = "let FOD_CO = class { constructor(){};getbrowser_height = function(){alert(window.innerHeight)}; getbrowserwidth = function(){alert(window.innerWidth);}; }; var fod_co = new FOD_CO(); fod_co.getbrowser_height(); fod_co.getbrowserwidth();"

        print(fd.javascript.javascript)

        self.assertEqual(fd.javascript.javascript.strip(), desired.strip())

    def test_javascript_bundler_no_js(self):

        print("Testing JavaScript bundler with no js")
            
        myPipleine = PipelineBuilder().add(NoJSFlowElement()).add(JavascriptBundler()).build()

        fd = myPipleine.createFlowData()

        fd.process()

        self.assertEqual(fd.javascript, None)
