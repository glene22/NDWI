# main.py

import glob
from ndwi_main import run_ndwi_analysis

# Match Sentinel-2 bands by wildcard
green_path  = glob.glob("example_data/*_B03.jp2")[0]   # Green (10m)
nir_path    = glob.glob("example_data/*_B08.jp2")[0]   # NIR (10m)
blue_path   = glob.glob("example_data/*_B02.jp2")[0]   # Blue (10m)
red_path    = glob.glob("example_data/*_B04.jp2")[0]   # Red (10m)
swir_path   = glob.glob("example_data/*_B11.jp2")[0]   # SWIR (20m)
cirrus_path = glob.glob("example_data/*_B10.jp2")[0]   # Cirrus (60m)

# Output directory
output_dir = "output/ndwi_results"

# Run NDWI analysis
run_ndwi_analysis(
    green_path=green_path,
    nir_path=nir_path,
    blue_path=blue_path,
    red_path=red_path,
    swir_path=swir_path,
    cirrus_path=cirrus_path,
    output_dir=output_dir,
    ndwi_thresh=0.16,
    min_size=10,
)
