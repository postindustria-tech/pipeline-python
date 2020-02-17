from fiftyone_pipeline_engines.engine import Engine
from fiftyone_pipeline_core.elementdata_dictionary import ElementDataDictionary
from fiftyone_pipeline_core.dataproperty_dictionary import DataPropertyDictionary

class JavascriptBundler(Engine):

    def __init__(self):

        super(JavascriptBundler, self).__init__()

        self.dataKey = "javascript"

        self.properties = DataPropertyDictionary(self)

        self.properties.addProperty("javascript", {
            "type": "string",
            "description": "Bundle of all javascript properties."
        })

    def sanitizeName(self, string):
            cleanstring = string.replace(".", "_").replace("-" , "_")
            return cleanstring

    def processInternal(self, flowData):
        javascript = flowData.getWhere(("type", "javascript"))

        output = ""

        if len(javascript) > 0:
            output += "let FOD_CO = class { constructor(){};"
            for propertykey, script in sorted(javascript.items()):

                # Check if straight value or a AspectPropertyValue

                if script.__class__.__name__ == "AspectPropertyValue":
                    if script.hasValue():
                        script = script.value()
                    else:
                        break

                propertykey = self.sanitizeName(propertykey)
                output += propertykey + " = function(){" + script + "}; "

            output += "}; "

            output += "var fod_co = new FOD_CO(); "

            for propertykey, script in sorted(javascript.items()):

                if script.__class__.__name__ == "AspectPropertyValue" and not script.hasValue():
                    break

                output += "fod_co." + self.sanitizeName(propertykey) + "(); "

            data = ElementDataDictionary(self, {"javascript" : output})

            flowData.setElementData(data)
