"""
 * CobblemonData.py
 * Holds the spawn data of pokemon.
 * 
 * Copyright (c) 2023, Thomas Truong
"""

class CobblemonData:
  """Spawn data of a pokemon.

  Contains three dictionaries that hold spawn data of a pokemon.

  Attributes:
    index: the Pokemon's number in the pokedex.
    spawns: the general information.
    conditions: the conditions that ALLOW spawning.
    anticonditions: the conditions that PREVENT spawning.
  """

  def __init__(self):
    """Initializes the instance with default values."""
    self.index = None

    # General information.
    self.spawns = {
      "pokemon": None,
      "presets": None,
      "context": None,
      "bucket": None,
      "level": None,
      "weight": None,
      "weightMultiplier": None
    }

    # Spawn conditions.
    self.conditions = {
      "dimensions": None,  # [List] of dimension IDs.
      "biomes": None,      # [List] of biome tags.
      "structures": None,  # [List] of structures.
      "moonPhase": None,   # [Int] Can be 0-7.
      "canSeeSky": "ANY",  # [str/bool] Whether sky needs to be above it. 

      "minX": None,
      "minY": None,
      "minZ": None,
      "maxX": None,
      "maxY": None,
      "maxZ": None,

      "minLight": None,
      "maxLight": None,

      "timeRange": "any",  # "any", "day", "night", "morning" or "0-1200,2000-3000" or "day-1200,1600-morning"
      "isRaining": None,
      "isThundering": None,

      "minWidth": None,            # Min width to spawn.
      "maxWidth": None,            # Max width to spawn.
      "minHeight": None,           # Min height to spawn.
      "maxHeight": None,           # Max height to spawn.
      "neededNearbyBlocks": None,  # [List] of blocks, at least one must be nearby. 
      "neededBaseBlocks": None,    # [List] of blocks, at least one must be the base block.

      "minDepth": None,
      "maxDepth": None,
      "fluidIsSource": None,  # Is it a source block?
      "fluidBlock": None      # The fluid it spawns in.
    }

    # Anti-conditions
    self.anticonditions = {
      "biomes": None,             # [List] of excluded biome tags.
      "structures": None,         # [List] of excluded structures.
      "neededNearbyBlocks": None  # [List] of blocks that cannot be nearby.
    }



  # Change dictionary values.
  def set_spawn(self, key: str, value: str):
    """Sets a key in the spawns dictionary.
    
    Sets a value to spawns[key].

    Args:
      key:
        The key used to access a value in the dictionary.
      value:
        The value to change to.
    """
    self.spawns[key] = value


  def set_condition(self, key: str, value: str):
    """Sets a key in the conditions dictionary.
    
    Sets a value to conditions[key].

    Args:
      key:
        The key used to access a value in the dictionary.
      value:
        The value to change to.
    """
    self.conditions[key] = value


  def set_anti_condition(self, key: str, value: str):
    """Sets a key in the anticonditions dictionary.
    
    Sets a value to anticonditions[key].

    Args:
      key:
        The key used to access a value in the dictionary.
      value:
        The value to change to.
    """
    self.anticonditions[key] = value



  # Value converters/getters: returns proper values for certain headers.
  def get_index(self) -> str:
    """Returns the Pokemon's number in the pokedex."""
    return self.index


  def get_weather(self) -> str:
    """Gets the whether based on isRaining and isThundering conditions.
    
    Checks isRaining and isThundering to determine if the weather
    condition is 'storm', 'rain', or 'clear'.

    Returns:
      The weather (storm, rain, or clear).
    """
    # Is thundering.
    if self.conditions["isThundering"] == "true":
      return "storm"
    # Is raining.
    elif self.conditions["isRaining"] == "true":
      return "rain"
    # Is not raining.
    elif self.conditions["isRaining"] == "false":
      return "clear"
    # No conditions listed, any is assumed.
    return "any"


  def get_requirements(self) -> str:
    """Returns a string of the spawn requirements.

    Creates a string that contains all of the requirements needed
    for the pokemon to spawn, i.e. "minY = 5, maxY = 60".

    Returns:
      The string with all the spawn requirements.
    """
    possible_reqs = ["minX", "minY", "minZ", "maxX", "maxY", "maxZ",
                     "minLight", "maxLight", "minWidth", "maxWidth",
                     "minHeight", "maxHeight", "minDepth", "maxDepth",
                     "fluidIsSource", "fluidBlock", "neededNearbyBlocks",
                     "neededBaseBlocks"]
    moon_phases = ["Full Moon", "Waning Gibbous", "Last Quarter",
                   "Waning Crescent", "New Moon", "Waxing Crescent",
                   "First Quarter", "Waxing Gibbous"]
    spawn_requirements = ""

    # Set up moon phase if exist.
    phase = self.conditions["moonPhase"]
    if phase is not None:
      spawn_requirements += "moonPhase = "
      # One phase given.
      if len(phase) == 1:
        spawn_requirements += f"{moon_phases[int(phase) - 1]}"
      # Multiple phases given.
      else:
        phases = phase.replace(" ", "").split(",")
        # Get all of the phase names.
        phase_names = []
        for p in phases:
          phase_names.append(moon_phases[int(p) - 1])
        spawn_requirements += f"{', '.join(phase_names)}"


    # For every requirement in possible_reqs.
    for req in possible_reqs:
      requirement_value = self.conditions[req]
      # Requirement exists.
      if requirement_value is not None:
        # Already a requirement, append WITH a comma.
        if spawn_requirements != "":
          spawn_requirements += f", {req} = {requirement_value}"
        # No requirement, append.
        else:
          spawn_requirements += f"{req} = {requirement_value}"

    return spawn_requirements


  def get_min_level(self) -> str:
    """Returns the minimum level the Pokemon spawns as.

    Gets the minimum level the pokemon spawns as from
    self.spawns["level"] and returns it.

    Returns:
      The min level as string.
    """
    return self.spawns["level"].split("-")[0]


  def get_max_level(self) -> str:
    """Returns the maximum level the Pokemon spawns as.

    Gets the maximum level the pokemon spawns as from
    self.spawns["level"] and returns it.

    Returns:
      The max level as string.
    """
    levels = self.spawns["level"].split("-")
    # No max explicitly given, i.e. "50" instead of "45-50".
    if len(levels) == 1:
      # Return min since its also max.
      return levels[0]
    # Else, return max level.
    return levels[1]


  def get_weight_multiplier(self) -> str:
    """Returns the weight multiplier with the condition.

    Format will be: multiplier IF [condition(s)].

    Returns:
      The "multiplier IF [condition(s)]" as a string.
    """
    # If the weightMultiplier exists.
    if self.spawns["weightMultiplier"] is not None:
      unclean_data = self.spawns["weightMultiplier"]
      # Clean up data.
      clean_data = unclean_data.replace("{", "")
      clean_data = clean_data.replace("}", "")
      clean_data = clean_data.replace("multiplier:", "")
      clean_data = clean_data.replace("condition:", "")
      clean_data = clean_data.strip()
      clean_data = clean_data.replace(":", " =")
      splitted_data = clean_data.split(",")

      # Format the data (multiplier IF [conditions])
      formatted_data = f"x{splitted_data[0]} IF [{splitted_data[1].strip()}"
      for item in splitted_data[2:]:
        formatted_data = formatted_data + ", " + item.strip()
      formatted_data = formatted_data + "]"

      return formatted_data
