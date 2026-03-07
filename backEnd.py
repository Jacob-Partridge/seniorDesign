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
        
        self.spices = { 'Spice 1': {"seconds/gram" : 0.0, # Fine Salt
                                   "currentlyHoused" : 1,
                                   "conversionConstant" : 1},

                        'Spice 2': {"seconds/gram" : 0.0, # Black Pepper
                                   "currentlyHoused" : 2,
                                   "conversionConstant" : 1},

                        'Spice 3': {"seconds/gram" : 0.0, # Garlic Powder
                                   "currentlyHoused" : 3,
                                   "conversionConstant" : 1},

                        'Spice 4': {"seconds/gram" : 0.0, # Onion Powder
                                   "currentlyHoused" : 4,
                                   "conversionConstant" : 1},

                        'Spice 5': {"seconds/gram" : 0.0, # Paprika
                                   "currentlyHoused" : 5,
                                   "conversionConstant" : 1},

                        'Spice 6': {"seconds/gram" : 0.0, # Cumin
                                  "currentlyHoused" : 6,
                                  "conversionConstant" : 1},

                        'Spice 7': {"seconds/gram" : 0.0, # Chili Powder
                                   "currentlyHoused" : 7,
                                   "conversionConstant" : 1},

                        'Spice 8': {"seconds/gram" : 0.0, # Cayenne Pepper
                                   "currentlyHoused" : 8,
                                   "conversionConstant" : 1},

                        'Spice 9': {"seconds/gram" : 0.0, # Dried Oregano
                                   "currentlyHoused" : 9,
                                   "conversionConstant" : 1},
                                          
                        'Spice 10': {"seconds/gram" : 0.0, # Brown Sugar
                                     "currentlyHoused" : 10,
                                     "conversionConstant" : 1}
        }

    def addSpice(self, spiceName, gramsPerSecond, currentlyHoused):
        self.spices[spiceName] = { "seconds/gram" : gramsPerSecond, "currentlyHoused" : currentlyHoused}

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

        if size is not "Grams":
                timeToRun = self.calculateSpiceTime(amount, size, self.spiceBox['seconds/gram'], self.spiceBox['conversionConstant'])
        else:
                timeToRun = amount * self.spiceBox['seconds/gram']

        if self.spiceBox['currentlyHoused'] % 2 == 0:
            self.turnServo.throttle[self.channel] = 0.2
            time.sleep(5)
            self.turnServo.throttle[self.channel] = 0.0
        else:
            self.turnServo.throttle[self.channel] = -0.2
            time.sleep(5)
            self.turnServo.throttle[self.channel] = 0.0
        return
    
    def calculateSpiceTime(self, amount: int, size: str, gramsPerSecond: float, conversionConstant: float):
        if size == "teaspoon":
            return (amount * conversionConstant) / gramsPerSecond
        elif size == "tablespoon":
            return (amount * conversionConstant) / gramsPerSecond
        # elif size == "cup":
        # return (amount * 128) / gramsPerSecond