# CSV Tool
## Description
- Extracts data from the Cobblemon data pack, QALPS, into a CSV file that contains spawn properties for the pokemon.<br>
  - Should also work for other Cobblemon data packs since they should follow the same template.<br>
- QALPS has some mistakes in the data file though, but it will be ignored.<br>
- QLAPS: https://modrinth.com/datapack/questionably-lore-accurate-pokemon-spawns

## Usage
1. Have a directory named "QALPS" in the same directory.
  - QALPS directory contains all the data files.
    - Data files are in *QuestionablyLoreAccuratePokemonSpawns/data/cobblemon/spawn_pool_world/*
2. Run CSVConverter.py to generate a CSV based on the data files.
  - Output file will be in the same directory and named *cobblemonQALPS.csv*



# Data File Checker
## Description
- Checks the data files for misplaced conditions.<br>

## Usage
1. Have a directory named "QALPS" in the same directory.
  - QALPS directory contains all the data files.
    - Data files are in *QuestionablyLoreAccuratePokemonSpawns/data/cobblemon/spawn_pool_world/*
2. Run DataChecker.py to check for misplaced conditions.
  - Output will be to the console.