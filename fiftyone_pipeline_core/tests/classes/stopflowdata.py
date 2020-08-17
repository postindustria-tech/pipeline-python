from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter

class StopFlowData(FlowElement):

    def __init__(self):

        super(StopFlowData, self).__init__()

        self.dataKey = "stop"

    def processInternal(self, flowData):

        flowData.stop()


    def getEvidenceKeyFilter(self):

        return BasicListEvidenceKeyFilter(["header.user-agent"])
