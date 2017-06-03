# !/usr/bin/python3
import json
import os
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

formats = ["mp4", "mov", "wmv", "m4v"]

# Determines if a file is a video
def isVideo(filename):
    if ("-sample." in filename):
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

# Move files to subdirectory corresponding to model name
toMove = {}
for (root, dirs, files) in os.walk(downloadDir):
    for filename in files:
        if (isVideo(filename)):
            # is a recognized name in the filename?
            model = ""
            for name in names:
                expected = name.replace(" ", ".")
                if (expected in filename):
                    model = name
            for name in aliases:
                expected = name.replace(" ", ".")
                if (expected in filename):
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
        shutil.move(src, trashDir)
