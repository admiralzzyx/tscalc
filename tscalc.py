#!/bin/python3

# WIP:  later on, make a GUI version of this

"""
BASELINE OVERLAND CONDITIONS
    normal luggage, on foot, at max speed, on clear roads

BASELINE MARITIME CONDITIONS
    fast ship, on clear seas, at max speed

Incompatibilities:
    >Any of any other category, except Category Rush, w/ any of Category Maritime.
    >Any two within the same category, except for those within Category Maritime.
    >Riverboat, Fast Ship, and Slow Ship are mutually incompatible.
    >Any of Category Rush with Riverboat.

The output of this calculator will be in effective miles per day.
"""
import sys

# CLASSES & FUNCTIONS
## Conditions
class travelCondition:
    def __init__(self, indicator, multiplier, category):
        self.indicator = indicator
        self.multiplier = multiplier
        self.category = category


def conditionInstantiate(inputString):
    indicatorList = [*inputString] #parsing

    multiplierSwitch={
        'l':0.83,   #(Luggage) Heavy Luggage
        'm':1.0,    #(Rush) Max Speed
        'a':0.66,   #(Rush) Relaxed/Avg Speed
        'f':1.0,    #(Means) On Foot
        'h':1.86,   #(Means) Horse
        'r':7.71,   #(Means) Horse Relays
        'o':0.4,    #(Means) Oxcart
        'p':0.66,   #(Means) Porter
        'c':2.25,   #(Means) Fast Cart
        't':0.315,  #(Medium) Rough Terrain
        'x':0.7,    #(Medium) Roadless
        'w':1.0,    #(Medium) Highway
        'b':0.32,   #(Maritime) Riverboat
        'z':1.0,    #(Maritime) Fast Ship
        's':0.38,   #(Maritime) Slow Ship
        'd':0.75    #(Maritime) Daylight Only
    }

    categorySwitch={
        'l':'lug',
        'm':'rus',
        'a':'rus',
        'f':'mns',
        'h':'mns',
        'r':'mns',
        'o':'mns',
        'p':'mns',
        'c':'mns',
        't':'med',
        'x':'med',
        'w':'med',
        'b':'mar',
        'z':'mar',
        's':'mar',
        'd':'mar'
    }

    conditionObjList = []
    for i in indicatorList:
        multiplier = multiplierSwitch.get(i, 1.0)
        category = categorySwitch.get(i, "Invalid_Category")
        condition = travelCondition(i, multiplier, category)
        conditionObjList.append(condition)

    return conditionObjList


## Treks
class trek:
    def __init__(self, conditionList):
        self.conditionList = conditionList
        # Checking if the Trek is Maritime or Land-based
        for i in self.conditionList:
            if i.category == 'mar':
                base = 196.07
                break
            else:
                base = 28.76

        # Getting MilesPerDay
        self.milesPerDay = base
        for i in conditionList:
            self.milesPerDay *= i.multiplier


def incompatibilityCheck(conditionList):
    incompatibleCategorySwitch={
        'lug':['mar'],
        'rus':['b'],
        'mns':['mar'],
        'med':['mar'],
        'mar':['lug', 'mns', 'med']
    }

    incompatibleIndicatorSwitch={
        'b':['z', 's'],
        'z':['b', 's'],
        's':['b', 'z']
    }

    # Repeat Indicator-Characters and/or Categories Check
    for i in conditionList:
        matchCount = 0
        for j in conditionList:
            if i.indicator == j.indicator or i.category == j.category:
                matchCount += 1
                if matchCount > 1:
                    print(f"Error: Repeat characters and/or categories found in inputed string.")
                    exit()

    bannedItem = []
    usedItem = []
    for i in conditionList:
        usedItem.append(i.category)
        usedItem.append(i.indicator)

        for j in incompatibleCategorySwitch.get(i.category, "Invalid_List"):
            bannedItem.append(j)
        bannedItem.append(incompatibleIndicatorSwitch.get(i.indicator, []))

    for i in bannedItem:
        for j in usedItem:
            if i == j:
                print(f"Incompatibilities found: '{i}' & '{j}' are incompatible.")
                exit()


# DRIVER PROGRAM
## Help Menu
if len(sys.argv) <= 1 or sys.argv[1] == "--help" or sys.argv[1] == "-h":
    with open('man.txt', "r+") as f:
        print(f"\n{f.read()}")
    exit()

## Processing Input
inputString = sys.argv[1].replace('-', '')
conditionList = conditionInstantiate(inputString)
trek = trek(conditionList)
incompatibilityCheck(conditionList)

print(f"{trek.milesPerDay} miles per day.")

exit()
