# !/usr/bin/python3
import json
import os
import re
import shutil
import sys

with open("config/paths.json") as pathConfig:
    paths = json.load(pathConfig)
    downloadDir = paths["downloadDir"]
    modelsDir = paths["modelsDir"]
    trashDir = paths["trashDir"]

with open("config/models.json") as modelConfig:
    models = json.load(modelConfig)
    names = []
    # alias -> standardized name
    aliases = {}
    for model in models["models"]:
        name = model["name"]
        names.append(name)
        if "aliases" in model:
            for alias in model["aliases"]:
                aliases[alias] = name

formats = ["avi", "m4v", "mov", "mp4", "mpg", "wmv"]

# Determines if a file is a video
def isVideo(filename):
    if re.search("-sample\.", filename, re.IGNORECASE):
        return False
    for fmt in formats:
        if (filename.endswith(fmt)):
            return True
    return False

# Prints a confirmation message with user input
def confirm(message):
    response = input(message)
    if (response == "Y" or response == "y"):
        return True
    return False

# Creates a regex pattern from a name
def createPattern(name):
    pattern = name.replace(" ", ".")
    return re.compile(pattern, re.IGNORECASE)

# Organize files into subdirectories
def main():
    # Move files to subdirectory corresponding to model name
    toMove = {}
    for (root, dirs, files) in os.walk(downloadDir):
        for filename in files:
            if (isVideo(filename)):
                # is a recognized name in the filename?
                model = ""
                for name in names:
                    pattern = createPattern(name)
                    if (pattern.search(filename)):
                        model = name
                for name in aliases:
                    pattern = createPattern(name)
                    if (pattern.search(filename)):
                        model = aliases[name]

                # determine destination directory
                src = os.path.join(root, filename)
                if (len(model) != 0):
                    print (filename + " -> " + model)
                    toMove[src] = os.path.join(modelsDir, model)
                #else:
                #    print ("Unknown model: \"" + path + "\"")

    if (len(toMove) != 0 and confirm("Move files to destination [y/N]? ")):
        for src in toMove:
            if not os.path.exists(toMove[src]):
                os.makedirs(toMove[src])
            dest = os.path.join(toMove[src], os.path.basename(src))
            if not os.path.exists(dest):
                shutil.move(src, toMove[src])

    # Clean up empty directories by moving to trash directory
    toRemove = []
    for (root, dirs, files) in os.walk(downloadDir):
        if (len(dirs) == 0):
            # Don't move current download
            isCurrentDownload = "data.xml" in files
            # Move directory if there are no video files
            containsVideo = True in [isVideo(f) for f in files]
            if (not isCurrentDownload and not containsVideo):
                print (root, files)
                toRemove.append(root)

    if (len(toRemove) != 0 and confirm("Move files to trash [y/N]? ")):
        for src in toRemove:
            dest = os.path.join(trashDir, os.path.basename(src))
            if not os.path.exists(dest):
                shutil.move(src, dest)
            else:
                i = 2
                renamed = dest + "(1)"
                while os.path.exists(renamed):
                    renamed = dest + "(" + str(i) + ")"
                    i += 1
                shutil.move(src, renamed)

if __name__ == "__main__":
    main()
