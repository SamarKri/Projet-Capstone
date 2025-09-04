
import os
import json
from pathlib import Path
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import folium
from tempfile import NamedTemporaryFile
from codecarbon import EmissionsTracker

# ----------------------------
# Configuration
# ----------------------------
OUTDIR = Path("./outputs")
OUTDIR.mkdir(exist_ok=True)
COPERNICUS_FILE = OUTDIR / "20250709000000-GOS-L4_GHRSST-SSTfnd-OISST_HR_REP-MED-v02.0-fv03.0.nc"
OUTPUT_HTML = OUTDIR / "SST_Mediterranee_map.html"
SUMMARY_FILE = OUTDIR / "summary.json"
IMPACT_FILE = OUTDIR / "impact_estimate.json"

# ----------------------------
# Ouverture du dataset
# ----------------------------
def open_dataset():
    if not COPERNICUS_FILE.exists():
        raise FileNotFoundError(f"Le fichier Copernicus n'existe pas : {COPERNICUS_FILE}")
    ds = xr.open_dataset(COPERNICUS_FILE)
    lat_name = "lat" if "lat" in ds.coords else "latitude"
    lon_name = "lon" if "lon" in ds.coords else "longitude"
    da = ds[list(ds.data_vars)[0]]  # première variable SST
    return da, lat_name, lon_name

# ----------------------------
# Statistiques rapides
# ----------------------------
def compute_basic_stats(da):
    arr = da.values
    if arr.ndim == 3:
        arr = arr[0, :, :]
    if np.all(np.isnan(arr)):
        return {'mean': np.nan, 'min': np.nan, 'max': np.nan, 'median': np.nan}
    return {
        'mean': float(np.nanmean(arr)),
        'min': float(np.nanmin(arr)),
        'max': float(np.nanmax(arr)),
        'median': float(np.nanmedian(arr))
    }

# ----------------------------
# Carte interactive Folium
# ----------------------------
def create_folium_map(da, stats, lat_name, lon_name, output_html):
    arr = da.values
    if arr.ndim == 3:
        arr = arr[0, :, :]
    arr = np.where(np.isfinite(arr), arr, np.nan)

    lat_vals = da[lat_name].values
    lon_vals = da[lon_name].values
    lat_mean = float(np.mean(lat_vals))
    lon_mean = float(np.mean(lon_vals))
    stats_clean = {k: float(v) if np.isfinite(v) else None for k, v in stats.items()}

    # Sous-échantillonnage pour performance
    max_pixels = 100
    step_lat = max(1, arr.shape[0] // max_pixels)
    step_lon = max(1, arr.shape[1] // max_pixels)
    arr_small = arr[::step_lat, ::step_lon]
    lat_small = lat_vals[::step_lat]
    lon_small = lon_vals[::step_lon]

    m = folium.Map(location=[lat_mean, lon_mean], zoom_start=5, tiles='CartoDB positron')
    popup_html = f"<b>SST Stats</b><br>Mean: {stats_clean['mean']:.2f} °C<br>Min: {stats_clean['min']:.2f} °C<br>Max: {stats_clean['max']:.2f} °C"
    folium.Marker([lat_mean, lon_mean], popup=popup_html).add_to(m)

    with NamedTemporaryFile(suffix='.png', delete=False) as tmpf:
        fig = plt.figure(figsize=(3, 3), dpi=100)
        plt.imshow(arr_small, origin='lower',
                   extent=[float(lon_small.min()), float(lon_small.max()),
                           float(lat_small.min()), float(lat_small.max())],
                   aspect='auto')
        plt.axis('off')
        fig.savefig(tmpf.name, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        folium.raster_layers.ImageOverlay(tmpf.name,
                                          [[float(lat_small.min()), float(lon_small.min())],
                                           [float(lat_small.max()), float(lon_small.max())]],
                                          opacity=0.6).add_to(m)

    m.save(output_html)
    return output_html

# ----------------------------
# Main
# ----------------------------
def main():
    tracker = EmissionsTracker(output_dir=str(OUTDIR), output_file="emissions_codecarbon.csv")
    tracker.start()

    da, lat_name, lon_name = open_dataset()
    stats = compute_basic_stats(da)
    print("Statistiques SST :", stats)

    # Sauvegarde des stats
    with open(SUMMARY_FILE, 'w') as f:
        json.dump(stats, f, indent=4)

    create_folium_map(da, stats, lat_name, lon_name, OUTPUT_HTML)
    print(f"Carte sauvegardée : {OUTPUT_HTML}")

    tracker.stop()

    # Récupération impact CO2
    impact = tracker.final_emissions_data
    impact_dict = {
        "emissions_kg": impact.emissions,
        "energy_consumed_kWh": impact.energy_consumed,
        "duration_s": impact.duration,
        "emissions_rate_kg_per_sec": impact.emissions_rate
    }

    with open(IMPACT_FILE, 'w') as f:
        json.dump(impact_dict, f, indent=4)

    print(f"Impact CO2 sauvegardé dans : {IMPACT_FILE}")
    print(f"CO₂ émis (kg): {impact_dict['emissions_kg']:.6f}, Énergie (kWh): {impact_dict['energy_consumed_kWh']:.6f}")

if __name__ == "__main__":
    main()
