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

class Evidence: 

    def __init__ (self, flowData):
        """
        evidence container constructor
        param: flowData parent flowData
        """
        self.evidence = {}

        self.flowData = flowData


    def set(self, key, value):
        """
        set - Set a single piece of evidence by its element and value
        param: string key
        param: mixed value
        """

        keep = False

        for flowElement in self.flowData.pipeline.flowElements:

            if flowElement.filterEvidenceKey(key):

                keep = True

 
        if keep:

            self.evidence[key] = value


    def setFromDict(self, incomingArray):
        """
        setArray - Helper function to set multiple pieces of evidence from a dict
        param: mixed[]
        """

        if not type(incomingArray) is dict:

             self.flowData.setError("core", "Must pass valid dictionary.")

        for key, value in incomingArray.items():

             self.set(key, value)

    def get(self, key):
        """
        get - Get a piece of evidence by key
        param: string key
        """

        if key in self.evidence:

            return self.evidence[key]

        else:

            return



    def getAll(self):
        """
        getAll - Get all evidence
        returns: mixed[]
        """

        return self.evidence

    


