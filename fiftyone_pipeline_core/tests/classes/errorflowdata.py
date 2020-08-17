
from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter


class ErrorFlowData(FlowElement):

    def __init__(self):

        super(ErrorFlowData, self).__init__()

        self.dataKey = "error"

    def processInternal(self, flowData):
  
        raise Exception("Something went wrong")


    def getEvidenceKeyFilter(self):

        return BasicListEvidenceKeyFilter(["header.user-agent"])
