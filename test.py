import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import time

# Create synthetic data with 100 entries for 5 time series
data_1 = np.random.rand(100) * 100
data_2 = np.random.rand(100) * 100
data_3 = np.random.rand(100) * 100
data_4 = np.random.rand(100) * 100
data_5 = np.random.rand(100) * 100

# List of datasets
datasets = [data_1, data_2, data_3, data_4, data_5]

# Track total time
start_time = time.time()

# Fit the model 5 times on 5 different time series
for data in datasets:
  model = ExponentialSmoothing(data, trend=None, seasonal=None)
  model.fit(smoothing_level=0.3, optimized=True)

end_time = time.time()

# Output the total time taken
print(f"Total time for 5 fits: {end_time - start_time:.4f} seconds")
