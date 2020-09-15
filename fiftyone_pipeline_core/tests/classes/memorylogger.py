from fiftyone_pipeline_core.logger import Logger

class MemoryLogger(Logger):

    def __init__(self, min_level="error", settings = {}):

        super(MemoryLogger, self).__init__(min_level, settings)

        self.memory_log = []

    def log_internal(self, level, log):

        self.memory_log.append(log)
