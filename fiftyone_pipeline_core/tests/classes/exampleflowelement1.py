

from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter

class ExampleFlowElement1(FlowElement):

    def __init__(self):

        super(ExampleFlowElement1, self).__init__()

        self.dataKey = "example1"

    def processInternal(self, flowData):

        self.properties = {"integer" : { "type": "int"} }

        data = ElementDataDictionary(self, {"integer" : 5})

        flowData.setElementData(data)
    
    def getEvidenceKeyFilter(self):

        return BasicListEvidenceKeyFilter(["header.user-agent"])
