from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter

class StopFlowData(FlowElement):

    def __init__(self):

        super(StopFlowData, self).__init__()

        self.datakey = "stop"

    def process_internal(self, flowdata):

        flowdata.stop()

    def get_evidence_key_filter(self):

        return BasicListEvidenceKeyFilter(["header.user-agent"])
