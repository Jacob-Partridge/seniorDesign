import time
from adafruit_servokit import ServoKit

class SpiceItUpBackend:
    def __init__(self):
        
        # Initialize the kit.
        kit = ServoKit(channels=16)

        #  Access the continuous rotation servo property on channel input
        spice_boxes = kit.continuous_servo
        
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

    def addRecipe(self, recipeName, spiceList):
        self.recipes[recipeName] = spiceList
        return

    def despenseSpice(self, spice: str, amount: int):
        try:
            spice_boxes = self.spices[spice]["currentlyHoused"]
        
        except KeyError:
            print(f"Spice '{spice}' not housed, please house spice and try again.")
            return

        if spice_boxes in range (0,1):
            channel = 0
        elif spice_boxes in range (2,3):
            channel = 1
        elif spice_boxes in range (4,5):
            channel = 2
        elif spice_boxes in range (6,7):
            channel = 3
        elif spice_boxes in range (8,9):
            channel = 4

        if spice_boxes % 2 == 0:
            spice_boxes.throttle = 0.2
            time.sleep(5)
            spice_boxes.throttle = 0.0
        else:
            spice_boxes.throttle = -0.2
            time.sleep(5)
            spice_boxes.throttle = 0.0
        return 