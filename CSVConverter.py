"""
 * CSVConverter.py
 * Converts .json Cobblemon data files into CSV.
 * 
 * Copyright (c) 2023, Thomas Truong
"""

import os, csv, json, CobblemonData
from typing import Union

# Directory to read data files from.
DATA_DIR = "./CobblemonData/"

# Contains all the headers and where to get the values.
HEADERS = {
  "No.": "getIndex",
  "Pokemon": "spawns/pokemon",
  "Biome": "conditions/biomes",
  "Excluded": "anticonditions/biomes",
  "Excluded Blocks": "anticonditions/neededNearbyBlocks",
  "Time": "conditions/timeRange",
  "Weather": "getWeather",
  "Context": "spawns/context",
  "Preset": "spawns/presets",
  "Requirements": "getRequirements",
  "Bucket": "spawns/bucket",
  "Weight": "spawns/weight",
  "Lv. Min": "getMinLevel",
  "Lv. Max": "getMaxLevel",
  "canseeSky": "conditions/canSeeSky" 
}


def main():
  # Create CSV in write mode.
  with open("CobblemonData.csv", "w") as csvFile:
    csvWriter = csv.writer(csvFile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Create headers.
    csvWriter.writerow(HEADERS.keys())

    # Gets and sorts directory.
    sortedDirectory = sorted(os.listdir(DATA_DIR))

    # For every fileName in directory.
    for fileName in sortedDirectory:
      # Obtain Pokemon Index.
      pIndex = str(int(fileName.split("_")[0]))
      pFile = open(DATA_DIR + fileName, "r")
      # Obtain json data.
      pData = json.load(pFile)

      for spawn in pData["spawns"]:
        # Create a temporary pokemon object that stores data.
        tempData = CobblemonData.CobblemonData()
        tempData.index = pIndex

        # Extract all general information if possible.
        for key in tempData.spawns.keys():
          if (key in spawn):
            tempData.setSpawn(key, cleanJsonValue(spawn[key]))

        # Extract all spawn conditions if possible.
        for key in tempData.conditions.keys():
          if (key in spawn["condition"]):
            tempData.setCondition(key, cleanJsonValue(spawn["condition"][key]))

        # Extract all anti-conditions if possible.
        for key in tempData.anticonditions.keys():
          if ("anticondition" in spawn):
            if (key in spawn["anticondition"]):
              tempData.setAnticondition(key, cleanJsonValue(spawn["anticondition"][key]))
        
        # Write all the information into the row.
        csvWriter.writerow(getHeaderValues(tempData))
        
      # Close file.
      pFile.close()


def cleanJsonValue(jsonVal: Union[str, float, list, bool, int]) -> Union[str, None]:
  """Returns cleaned version of JSON value.

  Removes brackets from JSON, extra quotations, and turns it into a string.

  Args:
    jsonVal:
      The JSON value to clean up.
  
  Returns:
    The clean JSON value or None if nothing given.
  """

  # Nothing given.
  if (len(str(jsonVal)) == 0):
    return

  # Convert to JSON string.
  clean = json.dumps(jsonVal)
  # Is a list (has open bracket), remove brackets.
  if (len(clean) >= 2 and clean[0] == "["):
    clean = clean[1:-1]
  # Get rid of "s.
  clean = clean.replace('"', '')

  # Clean up the biomes/block values. 
  clean = clean.replace("#minecraft", "")
  clean = clean.replace("#cobblemon", "")
  clean = clean.replace(":is_", "")
  clean = clean.replace("minecraft:", "")
  
  return clean


def getHeaderValues(pokeData: CobblemonData) -> list:
  """Returns the values of each header.
  
  Retrieves the value of each header and puts it into a list to return.

  Args:
    pokeData:
      The object that contains a Pokemon's data.

  Returns:
    The list of values of each header.
  """
  headerValues = []

  # For every header.
  for header in HEADERS:
    valueLocation = HEADERS[header].split("/")
    # Getter function has value.
    if (len(valueLocation) == 1):
      headerValues.append(getattr(pokeData, valueLocation[0])())
    # Dictionary has value.
    else:
      headerValues.append(getattr(pokeData,
                                  valueLocation[0])[valueLocation[1]])
      
  # Capitalize all the Pokemon names.
  headerValues[1] = headerValues[1].title()

  return headerValues



if __name__ == "__main__":
  main()
