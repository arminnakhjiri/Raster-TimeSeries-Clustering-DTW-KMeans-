# Raster Time-Series Clustering (DTW K-Means)

This repository provides a **Python workflow** for clustering raster pixel time series using **Dynamic Time Warping (DTW) K-Means**. The script identifies pixels with similar temporal patterns regardless of temporal shifts, making it particularly suitable for vegetation phenology, crop monitoring, and other remote sensing time-series applications.

---

## 📌 Overview

- **Input:** Multi-band time-series GeoTIFF
- **Method:** DTW K-Means clustering
- **Training:** Random pixel sampling
- **Normalization:** Per-pixel z-score normalization
- **Output:** Single-band raster of cluster labels

Unlike conventional Euclidean K-Means, DTW K-Means compares the *shape* of temporal profiles, making it robust to differences in the timing of seasonal events (see Fig. below).

<img width="654" height="924" alt="image" src="https://github.com/user-attachments/assets/fac46901-369d-430b-aeac-67dd172c6047" />

---

## 📂 Input Data

The input is a multi-band GeoTIFF where:

- Each band represents one observation date
- All bands are spatially aligned
- Every pixel contains a temporal profile

Example:

| Band | Date |
|------|------|
| 1 | 2021-03-18 |
| 2 | 2021-04-02 |
| 3 | 2021-04-17 |
| ... | ... |

The raster may contain NDVI, EVI, land surface temperature, radar backscatter, or any other temporal variable.

---

## 🧰 Python Dependencies

```bash
pip install rasterio numpy tslearn
```

---

## 🧪 Workflow

The script performs the following steps:

1. Read the input time-series raster.
2. Reshape the raster into pixel-wise time series.
3. Remove invalid pixels.
4. Normalize each time series using z-score normalization.
5. Randomly sample pixels for model training.
6. Train a DTW K-Means model.
7. Predict cluster membership for every valid pixel.
8. Export the resulting cluster map as a GeoTIFF.

---

## ⚙️ Parameters

The main parameters are:

```python
n_clusters = 30
sample_size = 60000
random_seed = 42
```

- **n_clusters:** Number of output clusters.
- **sample_size:** Number of randomly selected pixels used for model training.
- **random_seed:** Ensures reproducible sampling and clustering.

---

## 🧾 Output

The output is a single-band GeoTIFF where each pixel value represents its assigned cluster.

```
1 = Cluster 1
2 = Cluster 2
...
30 = Cluster 30
```

The raster preserves the spatial reference and georeferencing information of the input dataset.

---

## Applications

Typical applications include:

- Vegetation phenology mapping
- Crop type discrimination
- Land-cover temporal analysis
- Environmental monitoring
- Satellite image time-series analysis
- Unsupervised pattern discovery

---

## 📄 License

MIT License

---

## Author

**Armin Nakhjiri**

Remote Sensing Scientist

✉️ Nakhjiri.Armin@gmail.com

---

*Simple tools for efficient geospatial data processing.*
