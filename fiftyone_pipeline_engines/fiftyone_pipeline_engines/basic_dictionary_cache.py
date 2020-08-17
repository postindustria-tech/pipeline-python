from fiftyone_pipeline_engines.datakeyed_cache import DataKeyedCache

class BasicDictionaryCache(DataKeyedCache):
    
    def __init__(self):

        self.cache = {}

    def getCacheValue(self, key):
        if key in self.cache:
            return self.cache[key]
        else:
            return None

    def setCacheValue(self, key, value):
        self.cache[key] = value
