

from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter
from fiftyone_pipeline_core.aspectproperty_value import AspectPropertyValue

class APVFlowElement(FlowElement):

    def __init__(self):

        super(APVFlowElement, self).__init__()

        self.dataKey = "apv"

        self.properties = {"yes" : { "type": "string"} }
        self.properties = {"no" : { "type": "string"} }

    def processInternal(self, flowData):

        yes = AspectPropertyValue(value="yes")
        no = AspectPropertyValue(noValueMessage="no")

        data = ElementDataDictionary(self, {"yes": yes, "no": no})

        flowData.setElementData(data)
    
    def getEvidenceKeyFilter(self):

        return BasicListEvidenceKeyFilter(["header.user-agent"])
