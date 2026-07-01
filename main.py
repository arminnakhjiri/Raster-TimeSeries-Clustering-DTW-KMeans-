import numpy as np
import rasterio
from tslearn.clustering import TimeSeriesKMeans

# Inputs
input_raster = r"path/to/TimeSeries_Stack.tif"
output_raster = r"path/to/TimeSeries_Clusters.tif"

n_clusters = 30
sample_size = 60000
random_seed = 42

# Read raster
print("Reading raster...")

with rasterio.open(input_raster) as src:
    stack = src.read()  # (bands, rows, cols)
    profile = src.profile

bands, rows, cols = stack.shape

print(f"Bands: {bands}")
print(f"Rows: {rows}")
print(f"Cols: {cols}")

# Reshape to (pixels, time)
print("Reshaping data...")

X = stack.reshape(bands, rows * cols).T

# Remove invalid pixels
print("Finding valid pixels...")

valid_mask = np.all(np.isfinite(X), axis=1)
X_valid = X[valid_mask]

print(f"Valid pixels: {X_valid.shape[0]}")

# Z-score normalization
print("Normalizing time series...")

mean = X_valid.mean(axis=1, keepdims=True)
std = X_valid.std(axis=1, keepdims=True)

std[std == 0] = 1

X_valid = (X_valid - mean) / std

# Random sample for training
print(f"Selecting {sample_size:,} random samples...")

rng = np.random.default_rng(random_seed)

sample_idx = rng.choice(
    X_valid.shape[0],
    size=min(sample_size, X_valid.shape[0]),
    replace=False
)

X_sample = X_valid[sample_idx]

print(f"Training samples: {X_sample.shape[0]}")

# tslearn expects: (n_samples, time_steps, dimensions)
X_sample_ts = X_sample[:, :, np.newaxis]

# Train model
print("Training DTW K-Means...")

model = TimeSeriesKMeans(
    n_clusters=n_clusters,
    metric="dtw",
    random_state=random_seed,
    n_init=2,
    max_iter=20,
    verbose=True
)

model.fit(X_sample_ts)

print("Training completed.")

# Predict all pixels
print("Predicting clusters...")

X_all_ts = X_valid[:, :, np.newaxis]

labels = model.predict(X_all_ts)

print("Prediction completed.")

# Build output raster
print("Building output raster...")

cluster_map = np.zeros(rows * cols, dtype=np.int16)

cluster_map[valid_mask] = labels + 1

cluster_map = cluster_map.reshape(rows, cols)

# Save output
profile.update(
    count=1,
    dtype=rasterio.int16,
    compress="lzw"
)

print("Saving raster...")

with rasterio.open(output_raster, "w", **profile) as dst:
    dst.write(cluster_map, 1)

print("====================================")
print("Finished successfully.")
print(f"Output: {output_raster}")
print("====================================")
