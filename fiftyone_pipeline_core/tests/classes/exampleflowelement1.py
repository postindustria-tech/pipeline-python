

from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter

class ExampleFlowElement1(FlowElement):

    def __init__(self):

        super(ExampleFlowElement1, self).__init__()

        self.datakey = "example1"

    def process_internal(self, flowdata):

        self.properties = {"integer" : { "type": "int"} }

        data = ElementDataDictionary(self, {"integer" : 5})

        flowdata.set_element_data(data)
    
    def get_evidence_key_filter(self):

        return BasicListEvidenceKeyFilter(["header.user-agent"])
