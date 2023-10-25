"""
 * CSVConverter.py
 * Converts .json Cobblemon data files into CSV.
 * 
 * Copyright (c) 2023, Thomas Truong
"""

import os
import csv
import json
import CobblemonData
from typing import Union

# Directory to read data files from.
DATA_DIR = "./CobblemonData/"
# Name of the outputted spreadsheet.
CSV_NAME = "CobblemonData.csv"

# Contains all the headers and where to get the values.
HEADERS = {
  "No.": "get_index",
  "Pokemon": "spawns/pokemon",
  "Biome": "conditions/biomes",
  "Excluded Biomes": "anticonditions/biomes",
  "Excluded Blocks": "anticonditions/neededNearbyBlocks",
  "Structures": "conditions/structures",
  "Excluded Structs": "anticonditions/structures", 
  "Time": "conditions/timeRange",
  "Weather": "get_weather",
  "Context": "spawns/context",
  "Preset": "spawns/presets",
  "Requirements": "get_requirements",
  "Bucket": "spawns/bucket",
  "Weight": "spawns/weight",
  "Weight Multiplier": "get_weight_multiplier",
  "Lv. Min": "get_min_level",
  "Lv. Max": "get_max_level",
  "canseeSky": "conditions/canSeeSky" 
}


def main():
  # Create CSV in write mode.
  with open(CSV_NAME, mode = "w", encoding = "utf-8") as csv_file:
    csv_writer = csv.writer(csv_file, quotechar='"', quoting=csv.QUOTE_MINIMAL)
    # Create headers.
    csv_writer.writerow(HEADERS.keys())

    # Gets and sorts directory.
    sorted_directory = sorted(os.listdir(DATA_DIR))

    # For every file_name in directory.
    for file_name in sorted_directory:
      # Obtain Pokemon Index.
      p_index = str(int(file_name.split("_")[0]))
      p_file = open(DATA_DIR + file_name, mode = "r", encoding = "utf-8")
      # Obtain json data.
      p_data = json.load(p_file)

      for spawn in p_data["spawns"]:
        # Create a temporary pokemon object that stores data.
        temp_data = CobblemonData.CobblemonData()
        temp_data.index = p_index

        # Extract all general information if possible.
        for key in temp_data.spawns.keys():
          if key in spawn:
            temp_data.set_spawn(key, clean_json_value(spawn[key]))

        # Extract all spawn conditions if possible.
        for key in temp_data.conditions.keys():
          if key in spawn["condition"]:
            temp_data.set_condition(key, clean_json_value(spawn["condition"][key]))

        # Extract all anti-conditions if possible.
        for key in temp_data.anticonditions.keys():
          if "anticondition" in spawn:
            if key in spawn["anticondition"]:
              temp_data.set_anti_condition(key, clean_json_value(spawn["anticondition"][key]))

        # Write all the information into the row.
        csv_writer.writerow(getheader_values(temp_data))

      print(f"Done generating {CSV_NAME}.")

      # Close file.
      p_file.close()


def clean_json_value(json_value: Union[str, float, list,
                                       bool, int]) -> Union[str, None]:
  """Returns cleaned version of JSON value.

  Removes brackets from JSON, extra quotations, and turns it into a string.

  Args:
    json_value:
      The JSON value to clean up.
  
  Returns:
    The clean JSON value or None if nothing given.
  """

  # Nothing given.
  if len(str(json_value)) == 0:
    return

  # Convert to JSON string.
  clean = json.dumps(json_value)
  # Is a list (has open bracket), remove brackets.
  if (len(clean) >= 2 and clean[0] == "["):
    clean = clean[1:-1]
  # Get rid of "s.
  clean = clean.replace("\"", "")

  # Clean up the biomes/block/structure values.
  clean = clean.replace("#minecraft", "")
  clean = clean.replace("#cobblemon", "")
  clean = clean.replace(":is_", "")
  clean = clean.replace("minecraft:", "")
  if len(clean) > 0 and clean[0] == ":":
    clean = clean[1:]

  return clean


def getheader_values(poke_data: CobblemonData) -> list:
  """Returns the values of each header.
  
  Retrieves the value of each header and puts it into a list to return.

  Args:
    poke_data:
      The object that contains a Pokemon's data.

  Returns:
    The list of values of each header.
  """
  header_values = []

  # For every key-value pair in HEADERS.
  for kv_pair in HEADERS.items():
    # Extract the header location from kv_pair.
    value_location = kv_pair[1].split("/")
    # Getter function has value.
    if len(value_location) == 1:
      header_values.append(getattr(poke_data, value_location[0])())
    # Dictionary has value.
    else:
      header_values.append(getattr(poke_data, value_location[0])[value_location[1]])

  # Capitalize all the Pokemon names.
  header_values[1] = header_values[1].title()

  return header_values


if __name__ == "__main__":
  main()
