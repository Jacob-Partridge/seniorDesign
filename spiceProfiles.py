class profiles:
    """Salt, black pepper, garlic powder, onion powder, 
       paprika (smoked if possible), cumin, chili powder, 
       cayenne pepper, dried oregano, brown sugar"""
    
    def __init__(self):
        self.spices = {'salt': { "gram/seconds" : 0.0,
                                "currentlyHoused" : False},

                        'black pepper': { "gram/seconds" : 0.0,
                                         "currentlyHoused" : False},

                        'garlic powder': { "gram/seconds" : 0.0,
                                          "currentlyHoused" : False},

                        'onion powder': { "gram/seconds" : 0.0,
                                         "currentlyHoused" : False},

                        'paprika': { "gram/seconds" : 0.0,
                                    "currentlyHoused" : False},

                        'cumin': { "gram/seconds" : 0.0,
                                  "currentlyHoused" : False},

                        'chili powder': { "gram/seconds" : 0.0,
                                         "currentlyHoused" : False},

                        'cayenne pepper': { "gram/seconds" : 0.0,
                                           "currentlyHoused" : False},

                        'dried oregano': { "gram/seconds" : 0.0,
                                          "currentlyHoused" : False},
                                          
                        'brown sugar': { "gram/seconds" : 0.0,
                                        "currentlyHoused" : False}
        }

    def addSpice(self, spiceName, gramsPerSecond, currentlyHoused):
        self.spices[spiceName] = { "gram/seconds" : gramsPerSecond, "currentlyHoused" : currentlyHoused}