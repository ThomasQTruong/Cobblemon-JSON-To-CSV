import os, json

def main():
  # Directory to read data files from.
  DATA_DIR = "./CobblemonData/"

  # Gets and sorts directory.
  sortedDirectory = sorted(os.listdir(DATA_DIR))

  # All of the possible conditions in pData["spawns"]["conditions"]
  possible_conditions = ["dimensions", "biomes", "moonPhase", "canSeeSky", "minX", "minY", "minZ", "maxX",
                         "maxY", "maxZ", "minLight", "maxLight", "timeRange", "isRaining", "isThundering",
                         "minWidth", "maxWidth", "minHeight", "maxHeight", "neededNearbyBlocks",
                         "neededBaseBlocks", "minDepth", "maxDepth", "fluidIsSource", "fluidBlock"]

  # For every fileName in directory.
  for fileName in sortedDirectory:
    pFile = open(DATA_DIR + fileName, "r")
    # Obtain json data.
    pData = json.load(pFile)

    # For every condition in possible_conditions.
    for condition in possible_conditions:
      # If condition is outside of pData["spawns"]["conditions"].
      if (condition in pData["spawns"][0]):
        # Print error with file name and condition.
        print(f"ERROR: {fileName}: {condition} outside of condition.")

    # Close file.
    pFile.close()
    exit()


if __name__ == "__main__":
  main()
