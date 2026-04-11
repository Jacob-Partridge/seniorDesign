import time
# from adafruit_servokit import ServoKit

class SpiceItUpBackend:
    """ This class will handle all the backend logic for the spice dispensing machine, 
        including calculating the time to run the servo for each spice, as well as keeping 
        track of the spice recipes. """

    # Spice channel queues for the 5 spice channels, each channel can hold 2 spice boxes, 
    # So we can have 10 spice boxes in total
    channelOneQueue = []
    channelTwoQueue = []
    channelThreeQueue = []
    channelFourQueue = []
    channelFiveQueue = []

    def __init__(self):
        try: 
            print("Initializing backend...")
            """ salt, black pepper, garlic powder, onion powder, paprika, cumin, chili powder, cayenne pepper, dried oregano, brown sugar """
            # Initialize the kit.
            # kit = ServoKit(channels=16)
            #  Access the continuous rotation servo property on channel input
            # self.turnServo = kit.continuous_servo
            self.spiceBox = 0
            self.timeToRun = 0
            self.channel = 0
            self.spiceQueue = []
            self.recipes = {}
            
            
            # We got the flow rate for salt and are using it as a baseline for the other spices, 
            # We can adjust the flow rates as we test the machine and get more accurate measurements for each spice
            self.spices = { 'Salt': {"teaspoons/second" : 7.5, # Fine Salt
                                    "currentlyHoused" : 0,
                                    "conversionConstant" : 1},

                            'Black Pepper': {"teaspoons/second" : 7.5, # Black Pepper
                                    "currentlyHoused" : 1,
                                    "conversionConstant" : 1},

                            'Garlic Powder': {"teaspoons/second" : 7.5, # Garlic Powder
                                    "currentlyHoused" : -1,
                                    "conversionConstant" : 1},

                            'Onion Powder': {"teaspoons/second" : 7.5, # Onion Powder
                                    "currentlyHoused" : -1,
                                    "conversionConstant" : 1},

                            'Paprika': {"teaspoons/second" : 7.5, # Paprika
                                    "currentlyHoused" : -1,
                                    "conversionConstant" : 1},

                            'Cumin': {"teaspoons/second" : 7.5, # Cumin
                                    "currentlyHoused" : -1,
                                    "conversionConstant" : 1},

                            'Chili Powder': {"teaspoons/second" : 7.5, # Chili Powder
                                    "currentlyHoused" : -1,
                                    "conversionConstant" : 1},

                            'Cayenne Pepper': {"teaspoons/second" : 7.5, # Cayenne Pepper
                                    "currentlyHoused" : -1,
                                    "conversionConstant" : 1},

                            'Dried Oregano': {"teaspoons/second" : 7.5, # Dried Oregano
                                    "currentlyHoused" : -1,
                                    "conversionConstant" : 1},
                                            
                            'Brown Sugar': {"teaspoons/second" : 7.5, # Brown Sugar
                                        "currentlyHoused" : -1,
                                        "conversionConstant" : 1}
        }
            print("Backend initialized successfully.")
        except:
            print("Error initializing backend.")
            return
        return

    def addSpice(self, spiceName: str, teaspoonsPerSecond: float, currentlyHoused: int):
        self.spices[spiceName] = { "teaspoons/second" : teaspoonsPerSecond, "currentlyHoused" : currentlyHoused}
        return

    def addRecipe(self, recipeName: str, spiceList: list):
        self.recipes[recipeName] = spiceList
        return
    
    def calculateSpiceTime(self, amount: float, size: str, teaspoonsPerSecond: float):

        if size == "Teaspoons":
            return amount * teaspoonsPerSecond
        elif size == "Tablespoons":
            return (amount * 3) * teaspoonsPerSecond
        elif size == "Cups":
            return (amount * 48) * teaspoonsPerSecond
        else:
            print("Error in spice time calculation")
            return 0
        
    def changeSpiceLayouts(self, newLayout: dict):
        # Assuming we are using the list to update the spice layout in the order of the spice dictionary
        # As well as changing the buttons in the frontend to reflect the new spice layout
        for spice in self.spices:
            self.spices[spice]['currentlyHoused'] = newLayout[spice]
            spiceArrayForFrontend = [spice for spice in self.spices]
        return

    def despenseSpice(self, spice: str, amount: str, size: str):
        self.spiceBox = self.spices[f'{spice}']
        self.housed = self.spiceBox['currentlyHoused']
        amount = int(amount)
        print(f"Box: {self.housed}\nAmount: {amount}\nSize: {size}\n")

        if spice =="Empty":
            print(f"Can not dispense empty spice.")
            return
        
        if self.housed == -1:
            print(f"Spice '{spice}' not housed, please house spice and try again.")
            return

        if self.spiceBox['currentlyHoused'] in (0, 5):
            self.channel = 0
        elif self.spiceBox['currentlyHoused'] in (1,6):
            self.channel = 1
        elif self.spiceBox['currentlyHoused'] in (2,7):
            self.channel = 2
        elif self.spiceBox['currentlyHoused'] in (3,8):
            self.channel = 3
        elif self.spiceBox['currentlyHoused'] in (4,9):
            self.channel = 4

        self.timeToRun = self.calculateSpiceTime(amount, size, self.spiceBox['teaspoons/second'])
                
        if self.spiceBox['currentlyHoused'] % 2 == 0:
            # self.turnServo[self.channel].throttle = -0.2
            print("Turning servo forward...")
            time.sleep(self.timeToRun)
        else:
            # self.turnServo[self.channel].throttle = 0.2
            print("Turning servo backward...")
            time.sleep(self.timeToRun)

        # self.turnServo[self.channel].throttle = 0.0
        return True
    
    def getRecipes(self):
        self.recipe = {}
        with open('recipes.txt', 'r') as f:
            self.recipeTxt =  f.read()
            self.recipesTxt = self.recipeTxt.split('endRecipe')

        for recipes in range (0, len(self.recipesTxt) - 1):
            recipeSplit = self.recipesTxt[recipes].split('=')
            recipeName = recipeSplit[0]
            spiceList = recipeSplit[1].split(',')
            self.recipes[recipeName] = spiceList
        print(self.recipes)
        return
    
    def updateAmountGUI(self, currentVal, delta):
        print(f"Current Value: {currentVal}, Delta: {delta}")
        newValue = max(0, currentVal + delta) # Prevents negative amounts
        print(f"New Value: {newValue}")
        return newValue
