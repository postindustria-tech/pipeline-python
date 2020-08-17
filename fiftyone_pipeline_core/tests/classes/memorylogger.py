from fiftyone_pipeline_core.logger import Logger

class MemoryLogger(Logger):

    def __init__(self, minLevel="error", settings = {}):

        super(MemoryLogger, self).__init__(minLevel, settings)

        self.memoryLog = []

    def logInternal(self, level, log):

        self.memoryLog.append(log)
