import os
import zipfile
import logging

import arcpy

logging.basicConfig(level=logging.DEBUG)

dem_tile_format = "img"
nad83_coordinate_system = arcpy.SpatialReference(4269)  # NAD 83

def get_zips_in_folder(folder_path):
	"""
		Given a folder, returns the list of zipfiles, as complete paths, inside of it. Meant to be pointed to a folder with
		a full set of downloaded DEM tiles, compressed
	:param folder_path:
	:return:
	"""

	print("Determining Zips in Folder")
	all_files = os.listdir(folder_path)
	zips = []  # set up the blank zips list

	for l_file in all_files:  # look through all of the files
		if l_file.lower().endswith(".zip") and zipfile.is_zipfile(os.path.join(folder_path, l_file)):
			# confirm it's a zipfile - first by extension, then if the extension matches by zipfile's more robust method
			zips.append(os.path.join(folder_path, l_file))  # append it to the list to return
	return zips


def extract_tile_from_zip(zip_file_path, output_folder, tile_format):
	"""
		Given a zip file, extracts the actual DEM tile from it and places it in an output location
	:param zip_file_path:
	:param tile_format:
	:return:
	"""

	print("Extracting tiles from zips")
	zipped_tile = zipfile.ZipFile(zip_file_path)  # create the zip object
	compressed_files = zipped_tile.namelist()  # get the list of items inside of it

	extracted_files = []
	for name in compressed_files:  # iterate through all of the items
		if name.lower().endswith(tile_format.lower()):  # and if its filetype matches the one we're looking for
			zipped_tile.extract(name, output_folder)  # extract it
			extracted_files.append(os.path.join(output_folder, name))  # return the path

	return extracted_files


def find_and_extract_tile_zips(input_folder, output_folder, extension):
	"""
		Just a controller that runs the code to find all the zips and extract them

	:param input_folder:
	:param output_folder:
	:param extension:
	:return:
	"""

	zips = get_zips_in_folder(input_folder)
	if len(zips) == 0:
		logging.error("No tiles found in folder")
		raise FileNotFoundError("No tiles found in specified folder")  # TODO: Make this a subclassed error
	elif len(zips) == 1:
		logging.warning("Only one tile found - mosaic not necessary, but continuing")

	tiles = []
	for zipped_file in zips:
		tiles += extract_tile_from_zip(zipped_file, output_folder, extension)

	return tiles


def make_mosaic_from_tiles(dem_tiles_folder, mosaic_name, geodatabase, coordinate_system, make_gdb=True):

	if not arcpy.Exists(geodatabase):
		folder, name = os.path.split(geodatabase)
		arcpy.CreateFileGDB_management(folder, name)

	print("Making Mosaic Dataset")
	arcpy.CreateMosaicDataset_management(geodatabase, mosaic_name, coordinate_system, num_bands=1)
	mosaic_dataset = os.path.join(geodatabase, mosaic_name)

	print("Adding Tiles to Dataset")
	arcpy.AddRastersToMosaicDataset_management(mosaic_dataset, "Raster Dataset", dem_tiles_folder, update_overviews="UPDATE_OVERVIEWS")


def zipped_tiles_to_mosaic_dataset(input_folder, output_tile_folder, mosaic_geodatabase, mosaic_name, coordinate_system=nad83_coordinate_system, tile_format=dem_tile_format, make_gdb_if_no_exist=True):
	find_and_extract_tile_zips(input_folder, output_tile_folder, tile_format)
	make_mosaic_from_tiles(output_tile_folder, mosaic_name, mosaic_geodatabase, coordinate_system, make_gdb=make_gdb_if_no_exist)
