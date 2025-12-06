import os
import json
import shutil
from subprocess import PIPE, run #allows running any terminal command
import sys #allows interaction with the interpreter

GAME_DIR_PATTERN = "game" #targets the dir with "game"

def find_all_game_paths(source):
    game_paths = []
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)

        break

    return game_paths


def main(source, target):
    cwd = os.getcwd() #dir that we are running the py file from
    source_path = os.path.join(cwd, source) #use this for paths because you can't hard code due to diff os
    target_path = os.path.join(cwd, target) 

    game_paths = find_all_game_paths(source_path)
    print(game_paths)

if __name__ == "__main__": 
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only")
    source, target = args[1:]
    main(source, target)