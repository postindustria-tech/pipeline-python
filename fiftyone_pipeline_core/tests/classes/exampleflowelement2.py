
from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter



class ExampleFlowElement2(FlowElement):

    def __init__(self):

        super(ExampleFlowElement2, self).__init__()

        self.dataKey = "example2"

    def processInternal(self, flowData):

        data = ElementDataDictionary(self, {"integer": 7})

        flowData.setElementData(data)


    properties = {"integer2" : {
            "type" : "int"
        }
    }

    def getEvidenceKeyFilter(self):

        return BasicListEvidenceKeyFilter(["header.user-agent"])
