# cleavage
A simple personal media organizer that sorts your downloads into subdirectories of your choice.

## Configuration
The config directory contains JSON configuration files. You'll need to create your own version of each file without the `.template` suffix in order for the script to work.

### paths.json
This file contains the path information for the organizer script.
`downloadDir` is the directory containing your media files.
`modelsDir` is the location of the model subdirectories. These subdirectories are the destinations of the media files.
`trashDir` is where non-media files will be relocated.
The script does not remove any files from the file system. The purpose of the trash directory is to provide a single location that you can manually inspect before permanently removing the files.

### models.json
This file contains a list of models and aliases that are used to determine which files to move and where to move them. For example, if the configuration contains a model with the name `jane doe`, the script will locate files containing `jane.doe` as part of the filename and move them to the subdirectory `jane doe` under the directory defined by `modelsDir`.

`aliases` allows you to map multiple names to the same target directory. For example, if `jane doe` has an alias `jane dough`, then files containing `jane.dough` will be moved to the `jane doe` subdirectory.

## Running the organizer
```
python organizer.py
```
The script will output which files it intends to move as well as the destination directory. It will ask for confirmation before performing the move operation. The same applies for the cleanup step. The actions are printed to the screen and confirmation is obtained before any files are moved.
