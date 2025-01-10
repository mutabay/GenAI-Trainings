# Example 1

def bubble_sort(arr):
    n = len(arr)  # Get the number of elements in the array
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place, no need to check them
        for j in range(0, n - i - 1):
            # Swap if the element found is greater than the next element
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr  # Return the sorted array


# Example 2

import pandas as pd
import numpy as np

# Load weather data from a CSV file into a DataFrame
weather_df = pd.read_csv('april2024_station_data.csv')

# Convert DataFrame columns to NumPy arrays for faster computation
wind_speed = weather_df['wind_speed'].to_numpy()
wind_direction = weather_df['wind_direction'].to_numpy()

# Convert wind direction from degrees to radians using NumPy's built-in function for better performance
wind_direction_rad = np.deg2rad(wind_direction)
