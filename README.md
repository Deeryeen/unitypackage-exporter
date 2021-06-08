# unitypackage-exporter
A python script that can extract .unitypackage files. It's simple and works with most newer instances of python3 (3.8 and up) without any required modules.

Usage: `python3 main.py <yourfile.unitypackage>`

This will export every asset inside of the .unitypackage file into a folder with the same name. For temp file operations, it will also create temporary directory to work on extracting and copying the files over to the target folder. I'm thinking of adding an override for the target folder as well as a few options. But apart from that, I think it's OK for a first version.

Output:

![Terminal Output](https://filedn.eu/l4GwDJdu6t1bAxQhrNuaMiS/publicgithubimages/CLI%20Output.png)

Folder Structure:

![Folder Structure](https://filedn.eu/l4GwDJdu6t1bAxQhrNuaMiS/publicgithubimages/Final%20Folder%20Structure.png)

