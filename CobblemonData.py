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
      "weight": None
    }
    
    # Spawn conditions.
    self.conditions = {
      "dimensions": None,  # [List] of dimension IDs.
      "biomes": None,      # [List] of biome tags.
      "moonPhase": None,   # [Int] Can be 0-7.
      "canSeeSky": None,   # [Bool]Whether sky needs to be above it. 
      
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
      "neededNearbyBlocks": None  # [List] of blocks that cannot be nearby.
    }



  # Change dictionary values.
  def setSpawn(self, key: str, value: str):
    """Sets a key in the spawns dictionary.
    
    Sets a value to spawns[key].

    Args:
      key:
        The key used to access a value in the dictionary.
      value:
        The value to change to.
    """
    self.spawns[key] = value


  def setCondition(self, key: str, value: str):
    """Sets a key in the conditions dictionary.
    
    Sets a value to conditions[key].

    Args:
      key:
        The key used to access a value in the dictionary.
      value:
        The value to change to.
    """
    self.conditions[key] = value
  

  def setAnticondition(self, key: str, value: str):
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
  def getIndex(self) -> str:
    """Returns the Pokemon's number in the pokedex."""
    return self.index


  def getWeather(self) -> str:
    """Gets the whether based on isRaining and isThundering conditions.
    
    Checks isRaining and isThundering to determine if the weather
    condition is 'storm', 'rain', or 'clear'.

    Returns:
      The weather (storm, rain, or clear).
    """
    # Is thundering.
    if (self.conditions["isThundering"] == "true"):
      return "storm"
    # Is raining.
    elif (self.conditions["isRaining"] == "true"):
      return "rain"
    # Is not raining.
    elif (self.conditions["isRaining"] == "false"):
      return "clear"
    # No conditions listed, any is assumed.
    return "any"


  def getRequirements(self) -> str:
    """Returns a string of the spawn requirements.

    Creates a string that contains all of the requirements needed
    for the pokemon to spawn, i.e. "minY = 5, maxY = 60".

    Returns:
      The string with all the spawn requirements.
    """
    possible_reqs = ["minX", "minY", "minZ", "maxX", "maxY", "maxZ",
                     "minLight", "maxLight", "minWidth", "maxWidth", "minHeight",
                     "maxHeight", "minDepth", "maxDepth", "fluidIsSource", "fluidBlock",
                     "neededNearbyBlocks", "neededBaseBlocks"]
    moonPhases = ["Full Moon", "Waning Gibbous", "Last Quarter", "Waning Crescent",
                  "New Moon", "Waxing Crescent", "First Quarter", "Waxing Gibbous"]
    spawnRequirements = ""

    # Set up moon phase if exist.
    phase = self.conditions["moonPhase"]
    if (phase != None):
      spawnRequirements += f"moonPhase = {moonPhases[int(phase)]}"

    # For every requirement in possible_reqs.
    for req in possible_reqs:
      reqVal = self.conditions[req]
      # Requirement exists.
      if (reqVal != None):
        # Already a requirement, append WITH a comma.
        if (spawnRequirements != ""):
          spawnRequirements += f", {req} = {reqVal}"
        # No requirement, append.
        else:
          spawnRequirements += f"{req} = {reqVal}"

    return spawnRequirements


  def getMinLevel(self) -> str:
    """Returns the minimum level the Pokemon spawns as.

    Gets the minimum level the pokemon spawns as from
    self.spawns["level"] and returns it.

    Returns:
      The min level as string.
    """
    return self.spawns["level"].split("-")[0]
  

  def getMaxLevel(self) -> str:
    """Returns the maximum level the Pokemon spawns as.

    Gets the maximum level the pokemon spawns as from
    self.spawns["level"] and returns it.

    Returns:
      The max level as string.
    """
    levels = self.spawns["level"].split("-")
    # No max explicitly given, i.e. "50" instead of "45-50".
    if (len(levels) == 1):
      # Return min since its also max.
      return levels[0]
    # Else, return max level.  
    return levels[1]
