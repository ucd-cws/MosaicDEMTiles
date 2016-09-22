# DEM Extracter and Builder

This is a script that, when pointed to a directory of zipped NED/3DEP tiles, will extract just the DEM data and create
a mosaic dataset with the tiles.

## Usage

As currently written, the script can only use the .IMG format zipped tiles, so download those using the national map viewer
and download manager first (which will bulk download tiles into a folder). Then run the following

```python
import extract_and_mosaic
extract_and_mosaic.zipped_tiles_to_mosaic_dataset({folder with zipped tiles}, {folder to place extracted tiles}, {path to geodatabase for mosaic}, {mosaic dataset name})
```

The geodatabase does not need to exist - it will be created if it doesn't. The folder with zipped tiles can have other
files in it - they will be ignored if they aren't zips and don't contain a .IMG raster inside.

## Long-Term vision
This started out of a desire to provide a polygon area and specify a DEM resolution in order to get a stitched DEM back.
That process is complicated and requires many pieces, so I started with just the part that requires more hand work, but
which can easily be scripted. In the long-run, I'd like to build it toward that goal, but it will be in pieces. Feel free
to make pull requests with contributions toward that goal.