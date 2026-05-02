import time
from threading import Thread, Event
from adafruit_servokit import ServoKit


class SpiceItUpBackend:
    """ This class will handle all the backend logic for the spice dispensing
    machine, including calculating the time to run the servo for each spice,
    as well as keeping track of the spice recipes. """

    def __init__(self):
        try:
            """ salt, black pepper, garlic powder, onion powder, paprika, cumin
            ,chili powder, cayenne pepper, dried oregano, brown sugar """
            # Initialize the kit.
            kit = ServoKit(channels=16)
            #  Access the continuous rotation servo property on channel input
            self.turnServo = kit.continuous_servo
            self.spiceBox = 0
            self.timeToRun = 0
            self.spiceQueue = []
            self.recipes = {}

            # We got the flow rate for salt and are using it as a baseline for
            # the other spices, We can adjust the flow rates as we test the
            # machine and get more accurate measurements for each spice

            self.spices = {'Salt': {"teaspoons/second": 7.5,
                                    "currentlyHoused": -1,
                                    "conversionConstant": 1},

                           'Black Pepper': {"teaspoons/second": 7.5,
                                            "currentlyHoused": -1,
                                            "conversionConstant": 1},

                           'Garlic Powder': {"teaspoons/second": 7.5,
                                             "currentlyHoused": -1,
                                             "conversionConstant":  1},

                           'Onion Powder': {"teaspoons/second":  7.5,
                                            "currentlyHoused": -1,
                                            "conversionConstant":  1},

                           'Paprika': {"teaspoons/second":  7.5,
                                       "currentlyHoused": -1,
                                       "conversionConstant":  1},

                           'Cumin': {"teaspoons/second":  7.5,
                                     "currentlyHoused": -1,
                                     "conversionConstant":  1},

                           'Chili Powder': {"teaspoons/second":  7.5,
                                            "currentlyHoused": -1,
                                            "conversionConstant":  1},

                           'Ground Ginger': {"teaspoons/second":  7.5,
                                             "currentlyHoused": -1,
                                             "conversionConstant":  1},

                           'Dried Oregano': {"teaspoons/second":  7.5,
                                             "currentlyHoused": -1,
                                             "conversionConstant":  1},

                           'Brown Sugar': {"teaspoons/second":  7.5,
                                           "currentlyHoused": -1,
                                           "conversionConstant":  1}
                           }

        except Exception as e:
            return
        return

    def addRecipe(self, recipeName: str, spiceList: list):
        with open('recipes.txt', 'a') as f:
            f.write(f"{recipeName} = ")
            for spice in spiceList:
                f.write(f"{spice[0]} | {spice[1]} | {spice[2]}; ")
            f.write("endRecipe\n")
        return

    def calculateSpiceTime(self, amount: float, size: str,
                           teaspoonsPerSecond: float):

        if size == "Teaspoons":
            return amount * teaspoonsPerSecond
        elif size == "Tablespoons":
            return (amount * 3) * teaspoonsPerSecond
        elif size == "Cups":
            return (amount * 48) * teaspoonsPerSecond
        else:
            return 0

    def changeSpiceLayouts(self, newLayout: list):
        """Assuming we are using the list to update the spice
        layout in the order of the spice dictionaryAs well as changing the
        buttons in the frontend to reflect the new spice layout"""
        for key in self.spices.keys():
            if key in newLayout:
                self.spices[key]['currentlyHoused'] = newLayout.index(key) + 1
            else:
                self.spices[key]['currentlyHoused'] = -1

    def despenseSpice(self, spiceInfo: list, event: Event, errorMessage: list):
        try:
            channel = 0
            if str(spiceInfo[0]) == "Empty":
                raise ValueError('Cannot dispense\nempty spice')

            spiceBox = self.spices[f'{spiceInfo[0]}']
            housed = spiceBox['currentlyHoused']

            if housed == -1:
                raise ValueError('ERROR: \nMissing Spice:  (')

            if spiceBox['currentlyHoused'] in range(1, 6):
                channel = spiceBox['currentlyHoused'] + 10
            else:
                channel = spiceBox['currentlyHoused'] - 6

            timeToRun = self.calculateSpiceTime(float(spiceInfo[1]),
                                                spiceInfo[2],
                                                spiceBox['teaspoons/second'])

            # Now each thread references its own local channel and timeToRun
            self.turnServo[channel].throttle = .2
            time.sleep(timeToRun)
            self.turnServo[channel].throttle = 0.4
            return

        except Exception as e:
            errorMessage[0] = str(e)
            event.set()

    def dispenseRecipe(self, recipeSpices: list, event: Event,
                       errorMessage: str):
        try:
            self.threadList = []
            self.missingSpice = ''
            for i in range(len(recipeSpices[0])):
                spice = recipeSpices[0][i][0]
                if self.spices[spice]['currentlyHoused'] == -1:
                    self.missingSpice = self.missingSpice + f'{spice}, '

            if len(self.missingSpice) > 0:
                raise ValueError('ERROR: Missing Spice(s): '
                                 f'(\n{self.missingSpice}')

            for i in range(len(recipeSpices)):
                spice = recipeSpices[i]
                thread = Thread(target=self.despenseSpice, args=(spice[0],
                                                                 spice[1],
                                                                 spice[2],
                                                                 event,
                                                                 errorMessage))
                thread.start()
                self.threadList.append(thread)

            for thread in self.threadList:
                thread.join()
            return

        except Exception as e:
            errorMessage[0] = str(e)
            event.set()

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

                    # 3. Check if there are actually spices
                    # (handles "Recipe 2 =  ")
                    data_part = data_part.strip()
                    if data_part:
                        # Split by ';' to get each spice block
                        spice_strings = data_part.split(';')

                        for s in spice_strings:
                            s = s.strip()
                            if s:
                                # 4. Split by '|' to get Name, Amount, Unit
                                spice_details = [item.strip() for item
                                                 in s.split('|')]

                                if len(spice_details) == 3:
                                    recipe_spices.append(spice_details)

                    # 5. Store the list of spices in the dictionary
                    self.recipes[recipe_name] = recipe_spices

        except FileNotFoundError:
            print("Error: recipes.txt not found.")

        return self.recipes

    def updateAmountGUI(self, currentVal: float, delta: float):
        newValue = max(0, currentVal + delta)  # Prevents negative amounts
        return newValue

    def removeRecipe(self, recipeName: str):
        self.skipNext = False
        with open('recipes.txt', 'r') as f:
            lines = f.readlines()
        with open('recipes.txt', 'w') as f:
            for line in lines:
                if self.skipNext:
                    self.skipNext = False

                elif line.startswith(recipeName):
                    self.skipNext = True

                else:
                    f.write(line)
