import os
import numpy as np
import rasterio
from rasterio.features import shapes
from skimage import measure, morphology
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import shape


# ========= Band loading (scaled) =========
def load_band(path, scale_factor=0.0001):
    print(f"Loading band from {path}...")
    with rasterio.open(path) as src:
        data = src.read(1).astype("float32") * scale_factor
        profile = src.profile
    print(f"Loaded band with shape: {data.shape}")
    return data, profile


# ========= Index calculations =========
def calculate_ndwi(green, nir):
    print("Calculating NDWI...")
    np.seterr(divide='ignore', invalid='ignore')
    ndwi = (green - nir) / (green + nir)
    ndwi[np.isnan(ndwi)] = 0
    print("NDWI calculation complete.")
    return ndwi

def calculate_ndsi(green, swir):
    print("Calculating NDSI...")
    np.seterr(divide='ignore', invalid='ignore')
    ndsi = (green - swir) / (green + swir)
    ndsi[np.isnan(ndsi)] = 0
    print("NDSI calculation complete.")
    return ndsi


# ========= Mask creation =========
def create_rock_mask(ndsi, blue, green):
    print("Generating rock mask...")
    mask = np.where((ndsi < 0.9) & (blue > 0) & (blue < 0.4) & (green < 0.4), 1, 0)
    return mask.astype("uint8")

def create_cloud_mask(swir_cirrus, swir, blue, rock_mask):
    print("Generating cloud mask...")
    cloud = np.where(
        (swir_cirrus > 0.003) & (swir > 0.11) & (blue > 0.6) & (blue < 0.97),
        1,
        0,
    )
    cloud = np.where(rock_mask == 1, 0, cloud)
    return cloud.astype("uint8")

def create_lake_mask(ndwi, blue, red, green, cloud_mask, rock_mask, ndwi_thresh=0.16):
    print("Generating lake mask...")
    condition = (
        (ndwi > ndwi_thresh)
        & ((blue - red) / (blue + red) > 0.16)
        & ((green - red) > 0.08)
        & ((green - red) < 0.4)
        & ((blue - green) > 0.04)
    )
    lake = np.where(condition, 1, 0)
    lake = np.where((cloud_mask == 1) | (rock_mask == 1), 0, lake)
    return lake.astype("uint8")


# ========= Postprocessing and export =========
def clean_mask(mask, min_size=10):
    print(f"Cleaning mask: removing objects smaller than {min_size} px...")
    labeled = morphology.label(mask, connectivity=2)
    cleaned = morphology.remove_small_objects(labeled, min_size=min_size)
    return (cleaned > 0).astype("uint8")


def save_geotiff(path, array, profile):
    print(f"Saving GeoTIFF to {path}...")
    profile.update(driver="GTiff", dtype="float32", count=1)
    with rasterio.open(path, "w", **profile) as dst:
        dst.write(array.astype("float32"), 1)


def polygonize(mask, transform, crs, output_path):
    print("Polygonizing lake mask...")
    results = (
        {"properties": {"value": v}, "geometry": s}
        for s, v in shapes(mask, mask=mask.astype(bool), transform=transform)
        if v == 1
    )
    gdf = gpd.GeoDataFrame.from_features(list(results), crs=crs)
    gdf.to_file(output_path, driver="GeoJSON")
    print(f"Saved polygons to {output_path} ({len(gdf)} features).")


def plot_histogram(mask, transform, output_path, max_area_km2=0.2):
    print("Generating lake area histogram...")
    labeled = measure.label(mask, connectivity=2)
    props = measure.regionprops(labeled)

    # Calculate areas in km²
    pixel_area = transform[0] * -transform[4] / 1e6
    areas = [p.area * pixel_area for p in props if (p.area * pixel_area) <= max_area_km2]

    if not areas:
        print("No lakes found within specified area range.")
        return

    # Plot histogram
    plt.figure(figsize=(8, 5))
    plt.hist(areas, bins=40, color="skyblue", edgecolor="black")
    plt.title("Lake Area Distribution")
    plt.xlabel("Area (km²)")
    plt.ylabel("Count")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Histogram saved to {output_path}")


# ========= Main function =========
def run_ndwi_analysis(
    green_path,
    nir_path,
    blue_path,
    red_path,
    swir_path,
    cirrus_path,
    output_dir,
    ndwi_thresh=0.16,
    min_size=10,
):
    print("Starting NDWI lake detection workflow...\n")
    os.makedirs(output_dir, exist_ok=True)

    # Load and scale bands
    green, profile = load_band(green_path)
    nir, _ = load_band(nir_path)
    blue, _ = load_band(blue_path)
    red, _ = load_band(red_path)
    swir, _ = load_band(swir_path)
    cirrus, _ = load_band(cirrus_path)

    # 🔁 Resample SWIR and cirrus bands to match 10 m resolution
    from scipy.ndimage import zoom

    if swir.shape != green.shape:
        scale_factor_swir = green.shape[0] / swir.shape[0]
        swir = zoom(swir, scale_factor_swir, order=0)
        print(f"Resampled SWIR to {swir.shape}")

    if cirrus.shape != green.shape:
        scale_factor_cirrus = green.shape[0] / cirrus.shape[0]
        cirrus = zoom(cirrus, scale_factor_cirrus, order=0)
        print(f"Resampled cirrus to {cirrus.shape}")

    # Indices
    ndwi = calculate_ndwi(green, nir)
    ndsi = calculate_ndsi(green, swir)

    # Masks
    rock_mask = create_rock_mask(ndsi, blue, green)
    cloud_mask = create_cloud_mask(cirrus, swir, blue, rock_mask)
    lake_mask = create_lake_mask(ndwi, blue, red, green, cloud_mask, rock_mask, ndwi_thresh)
    lake_mask_clean = clean_mask(lake_mask, min_size=min_size)

    # Save outputs
    print("\nSaving output files...")
    save_geotiff(os.path.join(output_dir, "ndwi.tif"), ndwi, profile)
    save_geotiff(os.path.join(output_dir, "lake_mask.tif"), lake_mask_clean, profile)
    polygonize(
        lake_mask_clean,
        profile["transform"],
        profile["crs"],
        os.path.join(output_dir, "lake_polygons.geojson"),
    )
    plot_histogram(
        lake_mask_clean,
        profile["transform"],
        os.path.join(output_dir, "lake_area_histogram.png"),
    )

    print("\n✅ Processing complete. All outputs saved to:", output_dir)
