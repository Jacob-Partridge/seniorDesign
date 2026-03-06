import time
from adafruit_servokit import ServoKit

class SpiceItUpBackend:
    def __init__(self):
        """ salt, black pepper, garlic powder, onion powder, paprika, cumin, chili powder, cayenne pepper, dried oregano, brown sugar """
        # Initialize the kit.
        self.kit = ServoKit(channels=16)

        #  Access the continuous rotation servo property on channel input
        self.turnServo = self.kit.continuous_servo
        self.spiceBox = None
        
        self.spices = { 'Spice 1': {"gram/seconds" : 0.0,
                                   "currentlyHoused" : 1},

                        'Spice 2': {"gram/seconds" : 0.0,
                                   "currentlyHoused" : 2},

                        'Spice 3': {"gram/seconds" : 0.0,
                                   "currentlyHoused" : 3},

                        'Spice 4': {"gram/seconds" : 0.0,
                                   "currentlyHoused" : 4},

                        'Spice 5': {"gram/seconds" : 0.0,
                                   "currentlyHoused" : 5},

                        'Spice 6': {"gram/seconds" : 0.0,
                                  "currentlyHoused" : 6},

                        'Spice 7': {"gram/seconds" : 0.0,
                                   "currentlyHoused" : 7},

                        'Spice 8': {"gram/seconds" : 0.0,
                                   "currentlyHoused" : 8},

                        'Spice 9': {"gram/seconds" : 0.0,
                                   "currentlyHoused" : 9},
                                          
                        'Spice 10': {"gram/seconds" : 0.0,
                                     "currentlyHoused" : 10}
        }

    def addSpice(self, spiceName, gramsPerSecond, currentlyHoused):
        self.spices[spiceName] = { "gram/seconds" : gramsPerSecond, "currentlyHoused" : currentlyHoused}

    def addRecipe(self, recipeName, spiceList):
        self.recipes[recipeName] = spiceList
        return

    def despenseSpice(self, spice: str, amount: int, size: str):
        self.spiceBox = self.spices[f'{spice}']
        self.housed = self.spiceBox['currentlyHoused']
        print(f"Box: {self.housed}\nAmount: {amount}\nSize: {size}\n")
        if self.housed == 0:
            print(f"Spice '{spice}' not housed, please house spice and try again.")
            return

        if self.spiceBox['currentlyHoused'] in range (0,1):
            self.channel = 0
        elif self.spiceBox['currentlyHoused'] in range (2,3):
            self.channel = 1
        elif self.spiceBox['currentlyHoused'] in range (4,5):
            self.channel = 2
        elif self.spiceBox['currentlyHoused'] in range (6,7):
            self.channel = 3
        elif self.spiceBox['currentlyHoused'] in range (8,9):
            self.channel = 4

        if self.spiceBox['currentlyHoused'] % 2 == 0:
            self.turnServo.throttle[self.channel] = 0.2
            time.sleep(5)
            self.turnServo.throttle[self.channel] = 0.0
        else:
            self.turnServo.throttle[self.channel] = -0.2
            time.sleep(5)
            self.turnServo.throttle[self.channel] = 0.0
        return