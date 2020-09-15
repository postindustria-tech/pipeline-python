
from fiftyone_pipeline_core.flowelement import FlowElement
from fiftyone_pipeline_core.basiclist_evidence_keyfilter import BasicListEvidenceKeyFilter


class ErrorFlowData(FlowElement):

    def __init__(self):

        super(ErrorFlowData, self).__init__()

        self.datakey = "error"

    def process_internal(self, flowdata):
  
        raise Exception("Something went wrong")


    def get_evidence_key_filter(self):

        return BasicListEvidenceKeyFilter(["header.user-agent"])
