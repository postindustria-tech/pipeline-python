

from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter
from fiftyone_pipeline_core.aspectproperty_value import AspectPropertyValue

class APVFlowElement(FlowElement):

    def __init__(self):

        super(APVFlowElement, self).__init__()

        self.datakey = "apv"

        self.properties = {"yes" : { "type": "string"} }
        self.properties = {"no" : { "type": "string"} }

    def process_internal(self, flowdata):

        yes = AspectPropertyValue(value="yes")
        no = AspectPropertyValue(no_value_message="no")

        data = ElementDataDictionary(self, {"yes": yes, "no": no})

        flowdata.set_element_data(data)
    
    def get_evidence_key_filter(self):

        return BasicListEvidenceKeyFilter(["header.user-agent"])
