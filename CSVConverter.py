import os, csv, json, operator

def main():
  # Directory to read data files from.
  QALPS_DIR = "./QALPS/"
  
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
        pName = json.dumps(spawn["pokemon"]).replace('"', '')
        
        # Get and format biome(s).
        pBiomes = json.dumps(spawn["condition"]["biomes"])[1:-1].replace('"', '')
        
        # Get and format exclusion if exists.
        if ("anticondition" in spawn):
          pExcluded = json.dumps(spawn["anticondition"]["biomes"])[1:-1].replace('"', '')
        else:
          pExcluded = ""

        # Get and format time if exists.
        if ("timeRange" in spawn["condition"]):
          pTime = json.dumps(spawn["condition"]["timeRange"]).replace('"', '')
        else:
          pTime = "any"
        
        # Get and format weather if exists.
        if ("isRaining" in spawn["condition"]):
          if (json.dumps(spawn["condition"]["isRaining"]).replace('"', '') == "true"):
            pWeather = "rain"
          else:
            pWeather = "clear"
        else:
          pWeather = "any"

        # Get context.
        pContext = json.dumps(spawn["context"]).replace('"', '')

        # Get preset(s) if exist.
        if ("presets" in spawn):
          pPresets = json.dumps(spawn["presets"])[1:-1].replace('"', '')
        else:
          pPresets = ""

        # Get and format requirement(s).
        if ("minY" in spawn["condition"]):  # Get minY if exists.
          pMinY = json.dumps(spawn["condition"]["minY"]).replace('"', '')
          pMinY = "minY = " + pMinY
        else:
          pMinY = ""
        if ("maxY" in spawn["condition"]):  # Get maxY if exists.
          pMaxY = json.dumps(spawn["condition"]["maxY"]).replace('"', '')
          pMaxY = "maxY = " + pMaxY
        else:
          pMaxY = ""
        if ("minLight" in spawn["condition"]):  # Get minLight if exists.
          pMinLight = json.dumps(spawn["condition"]["minLight"]).replace('"', '')
          pMinLight = "minLight = " + pMinLight
        else:
          pMinLight = ""
        if ("neededNearbyBlocks" in spawn["condition"]): # Get required blocks if exists.
          pReqBlocks = json.dumps(spawn["condition"]["neededNearbyBlocks"])[1:-1].replace('"', '')
        else:
          pReqBlocks = ""
        pRequirement = ", ".join(filter(None, [pMinY, pMaxY, pMinLight, pReqBlocks]))

        # Get bucket.
        pBucket = json.dumps(spawn["bucket"]).replace('"', '')
        
        # Get Weight.
        pWeight = json.dumps(spawn["weight"]).replace('"', '')
        
        # Get level range.
        pLvRange = json.dumps(spawn["level"]).replace('"', '').split("-")
        pLvMin = pLvRange[0]
        pLvMax = pLvRange[1]

        # Get seeSky attribute.
        if ("canSeeSky" in spawn["condition"]):
          pSeeSky = json.dumps(spawn["condition"]["canSeeSky"]).replace('"', '')
        else:
          pSeeSky = ""
        
        # Write all the information into the row.
        csvWriter.writerow([pIndex, pName, pBiomes, pExcluded, pTime, pWeather, pContext, pPresets,
                             pRequirement, pBucket, pWeight, pLvMin, pLvMax, pSeeSky])
      
      # Close file.
      pFile.close()


if __name__ == "__main__":
  main()
