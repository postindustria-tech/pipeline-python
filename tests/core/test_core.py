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

from fiftyone_pipeline_core.dataproperty_dictionary import DataPropertyDictionary
from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter
from fiftyone_pipeline_core.logger import Logger

myLogger = Logger(minLevel="debug")


###########################################
# Dummy User FlowElement 
class UserFlowElement(FlowElement):
    def __init__(self):

        # run the parent class' __init__
        super(UserFlowElement, self).__init__()

        # set the FlowElement's dataKey
        self.dataKey = "user"

        # set the FLowElement's properties
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
        self.properties.addProperty("shoeSize", {
            "type": "int",
            "description": "The user's shoe size."
        })

        # fake a database of users
        self.database = {
            "U001": {
                "firstName": "Rodderick",
                "lastName": "Jones",
                "age"   : 12,
                "shoeSize": 5
            },
            "U002": {
                "firstName": "Sally",
                "lastName": "Jones",
                "age": 23,
                "shoeSize": 12
            }
        }


    # define the processing to run in the .process() phase
    def processInternal(self, flowData):

        userID = flowData.evidence.get("userID")

        user = self.database[userID]

        data = ElementDataDictionary(self, user)

        flowData.setElementData(data)

    # add an evidence filter
    def getEvidenceKeyFilter(self):

        return BasicListEvidenceKeyFilter(["userID"])




###########################################
# Dummy User FlowElement to force an error
class ErrorFlowData(FlowElement):

    def __init__(self):

        super(ErrorFlowData, self).__init__()

        self.dataKey = "throwError"



    def processInternal(self, flowData):

        raise Exception("Something went wrong")

###########################################
# Dummy User FlowElement to stop processing
class StopFlowData(FlowElement):

    def __init__(self):

        super(StopFlowData, self).__init__()

        self.dataKey = "stopThis"

    def processInternal(self, flowData):

        flowData.stop()

###########################################
# Dummy User FlowElement to ensure processing stops
class NeverRunFlowData(FlowElement):

    def __init__(self):

        super(NeverRunFlowData, self).__init__()

        self.dataKey = "neverRun"

    def processInternal(self, flowData):

        data = ElementDataDictionary(self, {"no" : False})

        flowData.setElementData(data)


######################################
# The Tests

class CoreTests(unittest.TestCase):

    # Instantiate the USER FLowElement 
    fe = UserFlowElement()

    # Call PipelineBuilder to add the USER pipeline, and build the pipeline
    userPipeline = PipelineBuilder().add(fe).build()


    def test_flowdata_properties(self):
        """
        Test: Does the FlowData correctly get it's properties
        """
        print("Flowdata has propereties")

        # get all the properties a flowElement can produce
        flow_properties = self.fe.getProperties().getContents()

        # TEST: are there 4 properties? 
        self.assertEqual(len(flow_properties), 4)

        # TEST: pick a random peoperty - does it match?
        self.assertEqual(flow_properties['lastname']['description'], "The user's last name.")


    def test_pipeline_properties(self):
        """
        Test: Does the Pipeline correctly get it's properties
        """
        print("Pipeline has propereties")

        # get all the properties a flowElement can produce from the pipeline
        pipeline_properties = self.userPipeline.getProperties()

        # TEST: are there properties for the the flowElement
        self.assertEqual(len(pipeline_properties), 1)

        user_flowelement_properties_on_pipeline = pipeline_properties["user"].getContents()

        # get all the properties a the user flowElement can produce from the flow element
        user_flowelement_properties = self.fe.getProperties().getContents()
        
        # TEST: are they the same?
        self.assertEqual(user_flowelement_properties_on_pipeline, user_flowelement_properties)
        

    # create the pipeline's flowData
    fd = userPipeline.createFlowData()

    # set evidence that is not filtered out
    fd.evidence.set("userID", "U001")

    # set evidence that is filtered out
    fd.evidence.set("favouriteMammoth", "henrietta") # this is never actually set because none of the flowElements in the pipeline need it (evidenceKeyFilter)


    def test_evidence(self):
        """
        Test: Set and get FLowData evidence
        """
        print("FlowData evidence set and get")


        # TEST: is the non filtered evidence set?
        self.assertEqual(self.fd.evidence.get("userID"), "U001")
        
        # TEST: is the filtered evidence NOT set?
        self.assertIsNone(self.fd.evidence.get("favouriteMammoth"))
        

    def test_process_pipeline(self):
        """
        Test: Process the pipeline and get data back
        """
        print("Process pipeline and get data back")
        
        # process the pipeline
        self.fd.process()

        # get the result data for user's firstname
        self.assertEqual(self.fd.get("user").get("firstName"), "Rodderick")

        # get the result data for user's firstname from element
        self.assertEqual(self.fd.getFromElement(self.fe).get("lastName"), "Jones")

        # No errors raised
        self.assertEqual(self.fd.errors, {})
 
        # filter results with getwhere - returns list of tuples
        integer_results = self.fd.getWhere(("type", "int"))


        # are there 2 int results
        self.assertEqual(len(integer_results), 2)

        # test the result values
        for intProperty, intvalue in integer_results.items():

            if intProperty == "age":
                self.assertEqual(intvalue, 12)

            if intProperty == "shoeSize":
                self.assertEqual(intvalue, 5)


    def test_error_in_pipeline(self):
        """
        Test: Process the pipeline and get data error back
        """
        print("Get data error")
   
        fd = self.userPipeline.createFlowData()
        fd.evidence.set("userID", "U123")

        fd.process()

        # Error raised
        self.assertNotEqual(fd.errors, {})


    def test_stop_and_error_processing(self):
        """
        Test: Process the pipeline and get data back
        """
        print("Test Stop and Error")

        userPipelineStop = PipelineBuilder().add(self.fe).add(ErrorFlowData()).add(StopFlowData()).add(NeverRunFlowData()).build()

        fd = userPipelineStop.createFlowData()

        fd.evidence.set("userID", "U001")

        fd.process()
  
        # TEST: intentional error setting an retrieval 
        self.assertIn('throwError', fd.errors)
    
        # TEST: process stop
        self.assertTrue(fd.stopped)
        self.assertNotIn('neverRun', fd.data.keys())
        