

from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder

from .memorylogger import MemoryLogger
from .exampleflowelement1 import ExampleFlowElement1
from .exampleflowelement2 import ExampleFlowElement2
from .stopflowdata import StopFlowData
from .errorflowdata import ErrorFlowData
from .apvflowelement import APVFlowElement


# Test Pipeline builder for use with unit tests
class TestPipeline():

    def __init__(self, suppressException = True):

        logger = MemoryLogger("info")
        self.flowElement1 = ExampleFlowElement1()
        self.pipeline = (PipelineBuilder())\
            .add(self.flowElement1)\
            .add(ErrorFlowData())\
            .add(APVFlowElement())\
            .add(StopFlowData())\
            .add(ExampleFlowElement2())\
            .add_logger(logger)\
            .build()
            
        self.pipeline.suppress_process_exceptions = suppressException
        self.flowdata = self.pipeline.create_flowdata()
        self.flowdata.evidence.add("header.user-agent", "test")
        self.flowdata.evidence.add("some.other-evidence", "test")
        self.pipeline.log("error", "test")
        self.flowdata.process()
