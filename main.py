# This script is to extract any files inside of a .unitypackage file.
# Please make sure you only use this on .unitypackage files you own.
# This will create a folder with the exact same name as the input file.
# Have fun!
# Used for creating the temp folder name.
from hashlib import md5
# Uncompressing .unityasset files.
import tarfile
# Gnarly file handling stuff.
from pathlib import Path
from shutil import copy2, rmtree
# Getting input from the user.
import argparse
from sys import exit
parser = argparse.ArgumentParser()
parser.add_argument('file', action='store', help='Path to the .unityasset file')
# parser.add_argument('-o', '--override', metavar='folder', action='store', default=None, help='Override default export location')
args = parser.parse_args()

unity_file = Path(args.file)
# There is probably a better way to just get the name of a file, but I'm lazy and want this to work.
unity_file_name = args.file.split('.')[:-1]
unity_file_name = '.'.join(unity_file_name)
# Does file exist?
if not unity_file.exists():
	print(f'File "{unity_file}" does not exist!')
	exit(1)

# Is file Valid? (Doesn't actually check magic nor the contents of the tar archive. This is just a dumb check)
if not unity_file.name.split('.')[-1] == 'unitypackage':
	print(f'File "{unity_file.name}" is not valid.')
	exit(1)

# Make target directory.
# Check if the target directory exists.
new_directory = Path(unity_file_name)
if new_directory.exists():
	# We don't want to overwrite a previous export.
	print('The target directory exists... Could it be possible that you\'ve already exported this asset file?')
	exit(1)

new_directory.mkdir(0o755, parents=True, exist_ok=False)

print('Initialized working environment.') # We just created the folders and checked some stuff, it's not like anything fancy really happened.
# Generate the temp directory name and pathlib object. This is an MD5 hash of the input filename.
tmp_dir_name = md5(unity_file_name.encode()).hexdigest()
tmp_dir = Path(tmp_dir_name)
# Extract to the temp directory.
unity_tar_file = tarfile.open(unity_file, mode='r:gz')
unity_tar_file.extractall(tmp_dir)
print(f'Read and extracted "{unity_file_name}"')

index=0
print('Processing extracted files...')
# Iterate through the directories.
for asset_directory in tmp_dir.iterdir():
	index=index+1
	# Generate links to asset elements known to be present.
	asset_file = Path(asset_directory, 'asset')
	# Check if it exists.
	if not asset_file.exists():
		# No need to make a fuss if it doesn't. Just continue.
		continue

	# Get original filename and directory structure.
	asset_path_name = Path(asset_directory, 'pathname')
	with open(asset_path_name, 'r') as f:
		pathname = f.read().split('/')

	new_asset_name = pathname[-1]
	new_dir_name = '/'.join(pathname[:-1])
	new_dir = Path(new_directory, new_dir_name)
	new_dir.mkdir(mode=0o755, parents=True, exist_ok=True)
	print(f'Found and copied {index} files...', end='\r')
	copy2(asset_file, Path(new_dir, new_asset_name))

print('\nDone processing the extracted files.')

rmtree(tmp_dir)
print('Cleaned up environment, enjoy!')