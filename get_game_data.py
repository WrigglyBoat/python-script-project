import os
import json
import shutil
from subprocess import PIPE, run #allows running any terminal command
import sys #allows interaction with the interpreter

GAME_DIR_PATTERN = "game" #targets the dir with "game"
GAME_CODE_EXT = ".go"
GAME_COMPILE_CMD = ["go", "build"]

def find_all_game_paths(source):
    game_paths = []
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break
    return game_paths

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)
    return new_names

def copy_overwrite(source, dest): #recurrsive
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)

def make_json_metadata(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberofGames": len(game_dirs)
    }

    with open(path, "w") as f:
        json.dump(data, f)

def compile_game_code(path): #assuming theres a single code file in each dir
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXT):
                code_file_name = file
                break #first one no need to keep looking
        break
    
    if code_file_name is None:
        return
    
    command = GAME_COMPILE_CMD + [code_file_name]
    run_command(command, path)

def run_command(command, path):
    cwd = os.getcwd()
    os.chdir(path)

    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True, shell=True)
    print("compile result", result)
    os.chdir(cwd)


def main(source, target):
    cwd = os.getcwd() #dir that we are running the py file from
    source_path = os.path.join(cwd, source) #use this for paths because you can't hard code due to diff os
    target_path = os.path.join(cwd, target) 

    game_paths = find_all_game_paths(source_path)
    new_game_dirs = get_name_from_paths(game_paths, "_game")
    create_dir(target_path)
    

    for src, dest in zip(game_paths, new_game_dirs): #zip takes matching elements from 2 arrays and gives access to both at the same time (tuple)
        dest_path = os.path.join(target_path,dest)
        copy_overwrite(src, dest_path)
        compile_game_code(dest_path)

    jsonPath = os.path.join(target_path, "metadata.json")
    make_json_metadata(jsonPath, new_game_dirs)
    

if __name__ == "__main__": 
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory - only")
    source, target = args[1:]
    main(source, target)