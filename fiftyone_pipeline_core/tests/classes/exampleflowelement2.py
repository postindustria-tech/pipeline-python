
from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter



class ExampleFlowElement2(FlowElement):

    def __init__(self):

        super(ExampleFlowElement2, self).__init__()

        self.datakey = "example2"

    def process_internal(self, flowdata):

        data = ElementDataDictionary(self, {"integer": 7})

        flowdata.set_element_data(data)


    properties = {"integer2" : {
            "type" : "int"
        }
    }

    def get_evidence_key_filter(self):

        return BasicListEvidenceKeyFilter(["header.user-agent"])
