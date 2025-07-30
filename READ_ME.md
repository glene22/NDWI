# NDWI-Based Supraglacial Lake Detection Framework

This repository contains a Python-based framework for detecting and mapping supraglacial lakes using Sentinel-2 imagery. The workflow uses the Normalized Difference Water Index (NDWI) alongside spectral masking techniques to identify water bodies while filtering out clouds, rock outcrops, and snow. It outputs binary lake masks, vector polygons, and lake area statistics.

The approach is adapted from the methodology presented in:

- Corr et al. (2022): *An inventory of supraglacial lakes and channels across the West Antarctic Ice Sheet*, ESSD, 14, 209–228. https://doi.org/10.5194/essd-14-209-2022  
- Glen et al. (2025): *A comparison of supraglacial meltwater features throughout contrasting melt seasons: southwest Greenland*, The Cryosphere, 19, 1047–1066. https://doi.org/10.5194/tc-19-1047-2025

---

## 🧭 Directory Structure

NDWI_Demo/
│
├── example_data/ # Example Sentinel-2 bands (JP2 or GeoTIFF)
├── output/ # Auto-generated outputs (lake masks, polygons, plots)
├── example_run.py # Example script for single-scene processing
├── ndwi_main.py # Main analysis module
├── requirements.txt # Required Python packages
├── README.md # This documentation file
└── example_outputs/ # (Optional) Pre-generated outputs for illustration


---
## Example Input & Output Files

You can download example input and output files from Google Drive:

[Example Input Data (Sentinel-2 JP2s)](https://drive.google.com/drive/folders/1mclEzTXcjgaKKyDqQQMiyZ9iqJZN8B8X?usp=drive_link)

[Example Output Files (lake mask, polygons, histogram)](https://drive.google.com/drive/folders/1ga7qYU_vSU0x903oA47CPPg6xe2GUd-C?usp=drive_link)

After downloading, place the files into:
- `example_data/` for input bands
- `example_outputs/` for sample results



## ✅ Features

- NDWI calculation from Green (B03) and NIR (B08) bands
- NDSI and multi-band spectral thresholds to filter clouds and rocks
- Customisable NDWI thresholding and minimum object size
- Nearest-neighbour resampling of 20 m and 60 m bands to 10 m
- Output of:
  - Binary lake masks (GeoTIFF)
  - Lake polygons (GeoJSON)
  - Area histograms (PNG)

---

## 🔧 Installation

This project requires Python 3.7 or later. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate         # Linux/macOS
venv\Scripts\activate            # Windows

pip install -r requirements.txt

▶️ Example Usage

To process the example Sentinel-2 scene included in example_data/, run:

python example_run.py

Ensure the following bands are present:

    B03 (Green)

    B08 (NIR)

    B02 (Blue)

    B04 (Red)

    B11 (SWIR)

    B10 (Cirrus)

    ⚙️ Parameters

You can adjust threshold values and object filtering by modifying the run_ndwi_analysis call in example_run.py.

run_ndwi_analysis(
    green_path=...,
    nir_path=...,
    blue_path=...,
    red_path=...,
    swir_path=...,
    cirrus_path=...,
    output_dir="output",
    ndwi_thresh=0.16,       # Adjust to make lake detection more/less strict
    min_size=10             # Minimum object size in pixels to retain
)


🖼️ Output Files

    ndwi.tif: NDWI index raster

    lake_mask.tif: Binary raster lake mask (cleaned)

    lake_polygons.geojson: Polygon vector file of detected lakes

    lake_area_histogram.png: Histogram of lake areas (km²)

By default, the histogram includes all detected lakes. To limit to, e.g., lakes < 2 km², you can modify the plot_histogram() function.

🗂️ Batch Mode (Optional)

This framework is designed for scalability. To apply the lake detection to multiple scenes:

    Organise each scene’s bands in a structured folder hierarchy.

    Loop through the folders and apply run_ndwi_analysis(...) with appropriate band paths.

    Store each output in a designated subfolder.

We can provide a batch_runner.py template upon request.
📚 Citation

If using this workflow in a publication, please cite the following:

    Corr, D., Leeson, A., McMillan, M., Zhang, C., and Barnes, T.: An inventory of supraglacial lakes and channels across the West Antarctic Ice Sheet, Earth Syst. Sci. Data, 14, 209–228, https://doi.org/10.5194/essd-14-209-2022, 2022.

    Glen, E., Leeson, A., Banwell, A. F., Maddalena, J., Corr, D., Atkins, O., Noël, B., and McMillan, M.: A comparison of supraglacial meltwater features throughout contrasting melt seasons: southwest Greenland, The Cryosphere, 19, 1047–1066, https://doi.org/10.5194/tc-19-1047-2025, 2025.

Maintained by Emily Glen. For questions, improvements, or collaboration:
e.glen@lancaster.ac.uk