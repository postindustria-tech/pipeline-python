

from fiftyone_pipeline_core.pipelinebuilder import PipelineBuilder

from .memorylogger import MemoryLogger
from .exampleflowelement1 import ExampleFlowElement1
from .exampleflowelement2 import ExampleFlowElement2
from .stopflowdata import StopFlowData
from .errorflowdata import ErrorFlowData
from .apvflowelement import APVFlowElement


# Test Pipeline builder for use with unit tests
class TestPipeline():

    def __init__(self):

        logger = MemoryLogger("info")
        self.flowElement1 = ExampleFlowElement1()
        self.pipeline = (PipelineBuilder())\
            .add(self.flowElement1)\
            .add(ErrorFlowData())\
            .add(APVFlowElement())\
            .add(StopFlowData())\
            .add(ExampleFlowElement2())\
            .addLogger(logger)\
            .build()
        self.flowData = self.pipeline.createFlowData()
        self.flowData.evidence.set("header.user-agent", "test")
        self.flowData.evidence.set("some.other-evidence", "test")
        self.pipeline.log("error", "test")
        self.flowData.process()
