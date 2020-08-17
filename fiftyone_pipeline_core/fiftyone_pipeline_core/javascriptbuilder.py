# *********************************************************************
# This Original Work is copyright of 51 Degrees Mobile Experts Limited.
# Copyright 2019 51 Degrees Mobile Experts Limited, 5 Charlotte Close,
# Caversham, Reading, Berkshire, United Kingdom RG4 7BY.
#
# This Original Work is licensed under the European Union Public Licence (EUPL)
# v.1.2 and is subject to its terms as set out below.
#
# If a copy of the EUPL was not distributed with this file, You can obtain
# one at https://opensource.org/licenses/EUPL-1.2.
#
# The 'Compatible Licences' set out in the Appendix to the EUPL (as may be
# amended by the European Commission) shall be deemed incompatible for
# the purposes of the Work and the provisions of the compatibility
# clause in Article 5 of the EUPL shall not apply.
#
# If using the Work as, or as part of, a network application, by
# including the attribution notice(s) required under Article 5 of the EUPL
# in the end user terms of the application under an appropriate heading,
# such notice(s) shall fulfill the requirements of that article.
# ********************************************************************


from .flowelement import FlowElement
from .evidence_keyfilter import EvidenceKeyFilter
from .elementdata_dictionary import ElementDataDictionary
import os
import json
import urllib.parse
import chevron
from jsmin import jsmin

"""
    The JavaScriptBuilder aggregates JavaScript properties
    from FlowElements in the Pipeline. This JavaScript also (when needed)
    generates a fetch request to retrieve additional properties
    populated with data from the client side
    It depends on the JSON Bundler element (both are automatically
    added to a Pipeline unless specifically removed) for its list of properties.
    The results of the JSON Bundler should also be used in a user-specified
    endpoint which retrieves the JSON from the client side.
    The JavaScriptBuilder is constructed with a url for this endpoint.

"""

class JavaScriptBuilderEvidenceKeyFilter(EvidenceKeyFilter):

    def filter(self, key):
        if "query" in key:
            return True

        if key == "header.host" or key == "header.protocol":
            return True
            
        return False


class JavascriptBuilderElement(FlowElement):


    def __init__(self, settings = {} ):
        """
        FlowData constructor.

        * @param {dict} options options object
        * @param {string} options.objName the name of the client
        * side object with the JavaScript properties in it
        * @param {string} options.protocol The protocol ("http" or "https")
        * used by the client side callback url.
        * This can be overriden with header.protocol evidence
        * @param {string} options.host The host of the client side
        * callback url. This can be overriden with header.host evidence.
        * @param {string} options.endPoint The endpoint of the client side
        * callback url
        * @param {boolean} options.enableCookies whether cookies should be enabled
        * @param {boolean} options.minify Whether to minify the JavaScript

        """

        super(JavascriptBuilderElement, self).__init__()

        self.settings = {}

        self.settings['_objName'] = settings["objName"] if "objName" in settings else 'fod'
        self.settings['_protocol'] = settings["protocol"] if "protocol" in settings else None
        self.settings['_host'] = settings["host"] if "host" in settings else None
        self.settings['_endpoint'] = settings["endpoint"] if "endpoint" in settings else ''
        self.settings['_enableCookies'] = settings["enableCookies"] if "enableCookies" in settings else True

        self.minify = settings["minify"] if "minify" in settings else True

        self.dataKey = "javascriptbuilder"

    """
    The JavaScriptBuilder captures query string evidence and
    headers for detecting whether the request is http or https
    
    """
    def getEvidenceKeyFilter(self):
   
        return JavaScriptBuilderEvidenceKeyFilter()

    """
    The JavaScriptBundler collects client side javascript to serve.

    @type FlowData: FlowData
    @param FlowData: The FlowData

    """
    def processInternal(self, flowData):
    
        variables = {}

        for key, value in self.settings.items():
            variables[key] = value

        variables["_jsonObject"] = json.dumps(flowData.jsonbundler.json)

        # Generate URL and autoUpdate params

        host = self.settings["_host"]
        protocol = self.settings["_protocol"]

        if not protocol:
            # Check if protocol is provided in evidence
            if flowData.evidence.get("header.protocol"):
                protocol = flowData.evidence.get("header.protocol")
            
        if not protocol:
            protocol = "https"
      

        if not host:
            # Check if host is provided in evidence

            if flowData.evidence.get("header.host"):
                host = flowData.evidence.get("header.host")

        variables["_host"] = host
        variables["_protocol"] = protocol

        if variables["_host"] and variables["_protocol"] and variables["_endpoint"]:

            variables["_url"] = variables["_protocol"] + "://" + variables["_host"] + variables["_endpoint"]

            # Add query parameters to the URL

            queryParams = self.getEvidenceKeyFilter().filterEvidence(flowData.evidence.getAll())

            query = {}
 
            for param, paramValue in queryParams.items():

                paramKey = param.split(".")[1] 

                query[paramKey] = paramValue
           
  
            urlQuery = urllib.parse.urlencode(query)
  
            # Does the URL already have a query string in it?
    
            if "?" not in variables["_url"]: 
                variables["_url"] += "?"
            else:
                variables["_url"] += "&"
            
            variables["_url"] += urlQuery

            variables["_updateEnabled"] = True
        else:
            variables["_updateEnabled"] = False
        

        # Use results from device detection if available to determine
        # if the browser supports promises.
        
        try:
            flowData.get("device").get("promise")
            variables["_supportsPromises"] = flowData.device.promise.value == True
        except Exception:
            variables["_supportsPromises"] = False
       
        # Check if any delayedproperties exist in the json

        variables["_hasDelayedProperties"] = True if "delayexecution" in variables["_jsonObject"] else False
         
        template = os.path.dirname(os.path.abspath(__file__)) + "/JavaScriptResource.mustache"
        
        with open(template, 'r') as f:
            output = chevron.render(f, variables)
        
        if self.minify:
            # Minify the output
            output = jsmin(output)
        
        data = ElementDataDictionary(self, {"javascript": output})

        flowData.setElementData(data)

        return
