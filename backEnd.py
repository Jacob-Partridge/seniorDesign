import time
from adafruit_servokit import ServoKit

class SpiceItUpBackend:
    def __init__(self):
        try: 
            print("Initializing backend...")
            """ salt, black pepper, garlic powder, onion powder, paprika, cumin, chili powder, cayenne pepper, dried oregano, brown sugar """
            # Initialize the kit.
            kit = ServoKit(channels=16)
            #  Access the continuous rotation servo property on channel input
            self.turnServo = kit.continuous_servo
            self.spiceBox = 0
            self.timeToRun = 0
            self.channel = 0
            self.spiceQueue = []
            self.recipes = {}
            self.spices = { 'Spice 1': {"teaspoons/second" : 1.0, # Fine Salt
                                    "currentlyHoused" : 1,
                                    "conversionConstant" : 1},

                            'Spice 2': {"teaspoons/second" : 1.0, # Black Pepper
                                    "currentlyHoused" : 2,
                                    "conversionConstant" : 1},

                            'Spice 3': {"teaspoons/second" : 1.0, # Garlic Powder
                                    "currentlyHoused" : 3,
                                    "conversionConstant" : 1},

                            'Spice 4': {"teaspoons/second" : 1.0, # Onion Powder
                                    "currentlyHoused" : 4,
                                    "conversionConstant" : 1},

                            'Spice 5': {"teaspoons/second" : 1.0, # Paprika
                                    "currentlyHoused" : 5,
                                    "conversionConstant" : 1},

                            'Spice 6': {"teaspoons/second" : 1.0, # Cumin
                                    "currentlyHoused" : 6,
                                    "conversionConstant" : 1},

                            'Spice 7': {"teaspoons/second" : 1.0, # Chili Powder
                                    "currentlyHoused" : 7,
                                    "conversionConstant" : 1},

                            'Spice 8': {"teaspoons/second" : 1.0, # Cayenne Pepper
                                    "currentlyHoused" : 8,
                                    "conversionConstant" : 1},

                            'Spice 9': {"teaspoons/second" : 1.0, # Dried Oregano
                                    "currentlyHoused" : 9,
                                    "conversionConstant" : 1},
                                            
                            'Spice 10': {"teaspoons/second" : 1.0, # Brown Sugar
                                        "currentlyHoused" : 10,
                                        "conversionConstant" : 1}
        }
            print("Backend initialized successfully.")
        except:
            print("Error initializing backend.")
            return
        
        return

    def addSpice(self, spiceName, teaspoonsPerSecond, currentlyHoused):
        self.spices[spiceName] = { "teaspoons/second" : teaspoonsPerSecond, "currentlyHoused" : currentlyHoused}
        return

    def addRecipe(self, recipeName, spiceList):
        self.recipes[recipeName] = spiceList
        return

    def despenseSpice(self, spice: str, amount: str, size: str):
        self.spiceBox = self.spices[f'{spice}']
        self.housed = self.spiceBox['currentlyHoused']
        amount = float(amount)
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

        if size == "Teaspoons":
            self.timeToRun = amount * self.spiceBox['teaspoons/second']
        else:
            self.timeToRun = self.calculateSpiceTime(amount, size, self.spiceBox['teaspoons/second'])
                
        if self.spiceBox['currentlyHoused'] % 2 == 0:
            self.turnServo.throttle[self.channel] = 0.2
            print("Turning servo forward...")
            time.sleep(self.timeToRun)
        else:
            self.turnServo.throttle[self.channel] = -0.2
            print("Turning servo backward...")
            time.sleep(self.timeToRun)

        self.turnServo.throttle[self.channel] = 0.0
        return
    
    def calculateSpiceTime(self, amount: float, size: str, teaspoonsPerSecond: float):
        if size == "Tablespoons":
            return (amount * 3) * teaspoonsPerSecond
        elif size == "Cups":
            return (amount * 48) * teaspoonsPerSecond
        else:
            return 0
        
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
