import time
from threading import Thread
# from adafruit_servokit import ServoKit

class SpiceItUpBackend:
    """ This class will handle all the backend logic for the spice dispensing machine, 
        including calculating the time to run the servo for each spice, as well as keeping 
        track of the spice recipes. """

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
                                    "currentlyHoused" : -1,
                                    "conversionConstant" : 1},

                            'Black Pepper': {"teaspoons/second" : 7.5, # Black Pepper
                                    "currentlyHoused" : -1,
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

                            'Ground Ginger': {"teaspoons/second" : 7.5, # Ground Ginger
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
        
    def changeSpiceLayouts(self, newLayout: list):
        # Assuming we are using the list to update the spice layout in the order of the spice dictionary
        # As well as changing the buttons in the frontend to reflect the new spice layout
        for key in self.spices.keys():
            if key in newLayout:
                self.spices[key]['currentlyHoused'] = newLayout.index(key) + 1
            else:
                self.spices[key]['currentlyHoused'] = -1


    def despenseSpice(self, spice: str, amount: str, size: str):
        if spice == "Empty":
            print(f"Can not dispense empty spice.")
            return
        
        self.spiceBox = self.spices[f'{spice}']
        self.housed = self.spiceBox['currentlyHoused']
        print(f"Box: {self.housed}\nAmount: {amount}\nSize: {size}\n")
        
        if self.housed == -1:
            print(f"Spice '{spice}' not housed, please house spice and try again.")
            return
        
        if self.spiceBox['currentlyHoused'] in range (1,9):
            self.channel = self.spiceBox['currentlyHoused'] - 1

        self.timeToRun = self.calculateSpiceTime(float(amount), size, self.spiceBox['teaspoons/second'])
                
        if self.spiceBox['currentlyHoused'] % 2 == 0:
            # self.turnServo[self.channel].throttle = -0.2
            print("Turning servo forward...")
            time.sleep(self.timeToRun)
        else:
            # self.turnServo[self.channel].throttle = 0.2
            print("Turning servo backward...")
            time.sleep(self.timeToRun)

        # self.turnServo[self.channel].throttle = 0.0
        return
    
    def dispenseRecipe(self, recipeSpices: list):
        for i in range(len(recipeSpices)):
            spice = recipeSpices[i][0]
            if self.spices[spice]['currentlyHoused'] == -1:
                print(f"Spice '{recipeSpices[i][0]}' not housed.")
                print(f"{self.spices[spice]['currentlyHoused']}")
                return
        for i in range(len(recipeSpices)):
            spice = recipeSpices[i]
            thread = Thread(target=self.despenseSpice, args=(spice[0], spice[1], spice[2]))
            thread.start()
        thread.join()
        return
    
    def getRecipes(self):
        self.recipes = {} 
        try:
            with open('recipes.txt', 'r') as f:
                # 1. Split by 'endRecipe' to get each block
                blocks = f.read().split('endRecipe')
                
            for block in blocks:
                block = block.strip()
                if '=' in block:
                    # 2. Separate "Recipe Name" from the "Spice Data"
                    name_part, data_part = block.split('=', 1)
                    recipe_name = name_part.strip()
                    
                    recipe_spices = []
                    
                    # 3. Check if there are actually spices (handles "Recipe 2 =  ")
                    data_part = data_part.strip()
                    if data_part: 
                        # Split by ';' to get each spice block
                        spice_strings = data_part.split(';')
                        
                        for s in spice_strings:
                            s = s.strip()
                            if s: # Ignore empty strings from trailing semicolons
                                # 4. Split by '|' to get Name, Amount, Unit
                                # This also strips extra spaces from each item automatically
                                spice_details = [item.strip() for item in s.split('|')]
                                
                                # Safety check: make sure we actually got 3 pieces of data
                                if len(spice_details) == 3:
                                    recipe_spices.append(spice_details)
                    
                    # 5. Store the list of spices in the dictionary
                    self.recipes[recipe_name] = recipe_spices
                    
        except FileNotFoundError:
            print("Error: recipes.txt not found.")
            
        return self.recipes
    
    def updateAmountGUI(self, currentVal, delta):
        print(f"Current Value: {currentVal}, Delta: {delta}")
        newValue = max(0, currentVal + delta) # Prevents negative amounts
        print(f"New Value: {newValue}")
        return newValue
