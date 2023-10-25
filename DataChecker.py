"""DataChecker.py

Used to check possible errors in data files.
"""

import os
import sys
import json


# Directory to read data files from.
DATA_DIR = "./CobblemonData/"


def main():
  error_count = 0

  # Gets and sorts directory.
  sorted_directory = sorted(os.listdir(DATA_DIR))

  # All of the possible conditions in p_data["spawns"]["conditions"]
  possible_conditions = ["dimensions", "biomes", "structures", "moonPhase",
                         "canSeeSky", "minX", "minY", "minZ", "maxX", "maxY",
                         "maxZ", "minLight", "maxLight", "timeRange",
                         "isRaining", "isThundering", "minWidth", "maxWidth",
                         "minHeight", "maxHeight", "neededNearbyBlocks",
                         "neededBaseBlocks", "minDepth", "maxDepth",
                         "fluidIsSource", "fluidBlock"]

  # For every file_name in directory.
  for file_name in sorted_directory:
    p_file = open(DATA_DIR + file_name, mode = "r", encoding = "utf-8")
    # Obtain json data.
    p_data = json.load(p_file)

    # For every condition in possible_conditions.
    for condition in possible_conditions:
      # If condition is outside of p_data["spawns"]["conditions"].
      if condition in p_data["spawns"][0]:
        # Print error with file name and condition.
        print(f"ERROR: {file_name}: {condition} outside of condition.")
        error_count += 1

    # Close file.
    p_file.close()

    print(f"Finished with {error_count} possible errors.")
    sys.exit()


if __name__ == "__main__":
  main()
