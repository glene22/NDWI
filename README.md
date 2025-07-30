# NDWI-Based Supraglacial Lake Detection Framework

This repository contains a Python-based framework for detecting and mapping supraglacial lakes using Sentinel-2 imagery. The workflow uses the Normalized Difference Water Index (NDWI) alongside spectral masking techniques to identify water bodies while filtering out clouds, rock outcrops, and snow. It outputs binary lake masks, vector polygons, and lake area statistics.

The approach is adapted from the methodology presented in:

- Corr et al. (2022): *An inventory of supraglacial lakes and channels across the West Antarctic Ice Sheet*, ESSD, 14, 209–228. https://doi.org/10.5194/essd-14-209-2022  
- Glen et al. (2025): *A comparison of supraglacial meltwater features throughout contrasting melt seasons: southwest Greenland*, The Cryosphere, 19, 1047–1066. https://doi.org/10.5194/tc-19-1047-2025

---

##  1. Directory Structure

```
project/
│
├── example_data/            # Example Sentinel-2 bands (JP2 or GeoTIFF)
├── output/                  # Auto-generated outputs (lake masks, polygons, plots)
├── example_run.py           # Example script for single-scene processing
├── ndwi_main.py             # Main analysis module
├── requirements.txt         # Required Python packages
├── README.md                # This documentation file
└── example_outputs/         # Pre-generated outputs for illustration
```
---

## 2. Example Input & Output Files

You can download example input and output files from Google Drive:

[Example Input Data (Sentinel-2 JP2s)](https://drive.google.com/drive/folders/1mclEzTXcjgaKKyDqQQMiyZ9iqJZN8B8X?usp=drive_link)

[Example Output Files (lake mask, polygons, histogram)](https://drive.google.com/drive/folders/1ga7qYU_vSU0x903oA47CPPg6xe2GUd-C?usp=drive_link)

After downloading, place the files into:
- `example_data/` for input bands
- `example_outputs/` for sample results

---
## 3. Features

- NDWI calculation from Green (B03) and NIR (B08) bands  
- Cloud and rock filtering using NDSI and multi-band spectral thresholds  
- Customisable NDWI threshold and minimum lake object size  
- Nearest-neighbour resampling of 20 m and 60 m bands to 10 m  
- Outputs:
  - Binary lake masks (GeoTIFF)
  - Polygon shapefiles of lakes (GeoJSON)
  - Area histograms (PNG)

---

## 4. Installation

This project requires **Python 3.7+**. To set up a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows

pip install -r requirements.txt
```

---

## 5. Example Usage

To process the example Sentinel-2 scene included in `example_data/`, run:

```bash
python example_run.py
```

### 6. Required Bands

Ensure the following Sentinel-2 bands are present:

- B03 (Green)  
- B08 (NIR)  
- B02 (Blue)  
- B04 (Red)  
- B11 (SWIR)  
- B10 (Cirrus)

---

###  7. Parameters

You can adjust threshold values and filtering in `example_run.py` by editing the `run_ndwi_analysis()` function call:

```python
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
```

---

## 8. Output Files

- `ndwi.tif`: NDWI raster  
- `lake_mask.tif`: Cleaned binary lake mask  
- `lake_polygons.geojson`: Vector polygons of detected lakes  
- `lake_area_histogram.png`: Histogram of lake areas (in km²)

> To limit the histogram to lakes below a certain size (e.g., <2 km²), edit the `plot_histogram()` function in `ndwi_main.py`.

---

## 9. Batch Mode (Optional)

To apply the lake detection to **multiple scenes**:

1. Organise each scene’s bands in a structured folder hierarchy.
2. Loop through the folders using a script.
3. Call `run_ndwi_analysis(...)` on each scene.
4. Save outputs in a dedicated subfolder.

---

## 10. Citation

If using this framework in a publication, please cite:

- Corr, D., Leeson, A., McMillan, M., Zhang, C., and Barnes, T.: *An inventory of supraglacial lakes and channels across the West Antarctic Ice Sheet*, Earth Syst. Sci. Data, 14, 209–228, https://doi.org/10.5194/essd-14-209-2022, 2022.  
- Glen, E., Leeson, A., Banwell, A. F., Maddalena, J., Corr, D., Atkins, O., Noël, B., and McMillan, M.: *A comparison of supraglacial meltwater features throughout contrasting melt seasons: southwest Greenland*, The Cryosphere, 19, 1047–1066, https://doi.org/10.5194/tc-19-1047-2025, 2025.

---

## 👤 Maintainer

**Emily Glen**  
e.glen@lancaster.ac.uk  
