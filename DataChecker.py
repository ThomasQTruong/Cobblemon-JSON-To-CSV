import os, json

def main():
  # Directory to read data files from.
  QALPS_DIR = "./QALPS/"

  # Gets and sorts directory.
  sortedDirectory = sorted(os.listdir(QALPS_DIR))

  # For every fileName in directory.
  for fileName in sortedDirectory:
    pFile = open(QALPS_DIR + fileName, "r")
    # Obtain json data.
    pData = json.load(pFile)

    for spawn in pData["spawns"]:
      # Check for misplaced conditions.
      if ("biomes" in spawn):
        print(fileName + ": biomes outside of condition.")
      if ("timeRange" in spawn):
        print(fileName + ": timeRange outside of condition.")
      if ("isRaining" in spawn):
        print(fileName + ": isRaining outside of condition.")
      if ("minY" in spawn):
        print(fileName + ": minY outside of condition.")
      if ("maxY" in spawn):
        print(fileName + ": maxY outside of condition.")
      if ("minLight" in spawn):
        print(fileName + ": minLight outside of condition.")
      if ("neededNearbyBlocks" in spawn):
        print(fileName + ": neededNearbyBlocks outside of condition.")
      if ("canSeeSky" in spawn):
        print(fileName + ": canSeeSky outside of condition.")

    # Close file.
    pFile.close()


if __name__ == "__main__":
  main()
