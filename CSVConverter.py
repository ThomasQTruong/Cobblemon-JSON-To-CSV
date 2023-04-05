"""
 * CSVConverter.py
 * Converts .json QALPS data files into CSV.
 * 
 * Copyright (c) 2023, Thomas Truong
"""

import os, csv, json, Pokemon

# Directory to read data files from.
QALPS_DIR = "./QALPS/"

def main():
  # Create CSV in write mode.
  with open("cobblemonQALPS.csv", "w") as csvFile:
    csvWriter = csv.writer(csvFile, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Create headers.
    csvWriter.writerow(["No.", "Pokemon", "Biome", "Excluded", "Time", "Weather", "Context", "Preset",
                         "Requirements", "Bucket", "Weight", "Lv. Min", "Lv. Max", "canseeSky"])

    # Gets and sorts directory.
    sortedDirectory = sorted(os.listdir(QALPS_DIR))

    # For every fileName in directory.
    for fileName in sortedDirectory:
      # Obtain Pokemon Index.
      pIndex = str(int(fileName.split("_")[0]))
      pFile = open(QALPS_DIR + fileName, "r")
      # Obtain json data.
      pData = json.load(pFile)

      for spawn in pData["spawns"]:
        # Get pokemon name.
        pName = cleanJsonValue(spawn["pokemon"]).capitalize()
        
        # Get and format biome(s).
        pBiomes = cleanJsonArray(spawn["condition"]["biomes"])
        
        # Get and format exclusion if exists.
        pExcluded = ""
        if ("anticondition" in spawn):
          pExcluded = cleanJsonArray(spawn["anticondition"]["biomes"])

        # Get and format time if exists.
        pTime = "any"
        if ("timeRange" in spawn["condition"]):
          pTime = cleanJsonValue(spawn["condition"]["timeRange"])
        
        # Get and format weather if exists.
        pWeather = "any"
        if ("isThundering" in spawn["condition"] and cleanJsonValue(spawn["condition"]["isThundering"]) == "true"):
          pWeather = "storm"
        elif ("isRaining" in spawn["condition"]):
          if (cleanJsonValue(spawn["condition"]["isRaining"]) == "true"):
            pWeather = "rain"
          else:
            pWeather = "clear"

        # Get context.
        pContext = cleanJsonValue(spawn["context"])

        # Get preset(s) if exist.
        pPresets = ""
        if ("presets" in spawn):
          pPresets = cleanJsonArray(spawn["presets"])

        # Get and format requirement(s).
        pMinY = ""
        pMaxY = ""
        pMinLight = ""
        pReqBlocks = ""
        if ("minY" in spawn["condition"]):  # Get minY if exists.
          pMinY = cleanJsonValue(spawn["condition"]["minY"])
          pMinY = "minY = " + pMinY
        if ("maxY" in spawn["condition"]):  # Get maxY if exists.
          pMaxY = cleanJsonValue(spawn["condition"]["maxY"])
          pMaxY = "maxY = " + pMaxY
        if ("minLight" in spawn["condition"]):  # Get minLight if exists.
          pMinLight = cleanJsonValue(spawn["condition"]["minLight"])
          pMinLight = "minLight = " + pMinLight
        if ("neededNearbyBlocks" in spawn["condition"]): # Get required blocks if exists.
          pReqBlocks = cleanJsonArray(spawn["condition"]["neededNearbyBlocks"])
        pRequirement = ", ".join(filter(None, [pMinY, pMaxY, pMinLight, pReqBlocks]))

        # Get bucket.
        pBucket = cleanJsonValue(spawn["bucket"])
        
        # Get Weight.
        pWeight = cleanJsonValue(spawn["weight"])
        
        # Get level range.
        pLvRange = cleanJsonValue(spawn["level"]).split("-")
        pLvMin = pLvRange[0]
        if (len(pLvRange) == 2):
          pLvMax = pLvRange[1]
        else:
          pLvMax = pLvMin

        # Get seeSky attribute.
        pSeeSky = ""
        if ("canSeeSky" in spawn["condition"]):
          pSeeSky = cleanJsonValue(spawn["condition"]["canSeeSky"])
        
        # Write all the information into the row.
        csvWriter.writerow([pIndex, pName, pBiomes, pExcluded, pTime, pWeather, pContext, pPresets,
                             pRequirement, pBucket, pWeight, pLvMin, pLvMax, pSeeSky])
      
      # Close file.
      pFile.close()


# Cleans the .json values.
def cleanJsonValue(jsonVal):
  return json.dumps(jsonVal).replace('"', '')


# Cleans the .json arrays.
def cleanJsonArray(jsonArr):
  return json.dumps(jsonArr)[1:-1].replace('"', '')


if __name__ == "__main__":
  main()
