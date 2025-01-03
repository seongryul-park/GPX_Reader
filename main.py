"""
File Name: main.py
Project: GPX_Reader

Author: Seongryul Park
Latest modifier: Seongryul Park

Creation date: 1/1/2025
Latest modified date: 1/2/2025
"""
from gpx_ver2 import GPX

try:
    file_path = "example.gpx"  # Replace with the path to your GPX file
    gpx = GPX(file_path)
    print("Total Distance (meters):", gpx.GetDistance())
    print("Min Elevation (meters):", gpx.GetMinElevation())
    print("Max Elevation (meters):", gpx.GetMaxElevation())
    print("Duration (seconds):", gpx.GetDuration())
    
    file_path2 = "example2.gpx"  # Replace with the path to your GPX file
    gpx2 = GPX(file_path2)
    print("Total Distance (meters):", gpx2.GetDistance())
    print("Min Elevation (meters):", gpx2.GetMinElevation())
    print("Max Elevation (meters):", gpx2.GetMaxElevation())
    print("Duration (seconds):", gpx2.GetDuration())
    
except ValueError as e:
    print(f"error: {e}")




    