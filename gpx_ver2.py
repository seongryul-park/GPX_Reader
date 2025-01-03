"""
File Name: gpx.py
Project: GPX_Reader

Author: Seongryul Park
Latest modifier: Seongryul Park

Creation date: 1/3/2025
Latest modified date: 1/3/2025

Description: GPX class uses for creation gpx object that can read gpx file and save file's track_points into its own class.
"""
import pandas as pd
import xml.etree.ElementTree as ET
from math import radians, cos, sin, sqrt, atan2

class GPX:
    # --- Private Functions -----------------------
    class __TrackPoint:
        def __init__(self, lat, lon, ele, time, hr):
            self.lat = float(lat)
            self.lon = float(lon)
            self.ele = ele
            self.time = time
            self.hr = hr

    def __Haversine(self, lat1, lat2, lon1, lon2, ele1, ele2):
        # Earth's radius
        radius = 6371.0

        lat1, lat2, lon1, lon2 = map(radians, [lat1, lat2, lon1, lon2])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        horizontal_distance = radius * c * 1000

        vertical_distance = abs(ele2 - ele1)

        return sqrt(horizontal_distance**2 + vertical_distance**2)

    def __TotalDistance(self):
        for i in range(1, len(self.track_df)):
            self.__v_total_distance += self.__Haversine(
                self.track_df.iloc[i - 1]["Latitude"],
                self.track_df.iloc[i]["Latitude"],
                self.track_df.iloc[i - 1]["Longitude"],
                self.track_df.iloc[i]["Longitude"],
                self.track_df.iloc[i - 1]["Elevation"],
                self.track_df.iloc[i]["Elevation"])

    def __ReadFile(self, filePath):
        # Initialize member variables
        self.__v_total_distance = 0.0
        self.__v_min_elevation = None
        self.__v_max_elevation = None
        self.__v_duration = None
    
        try:
            tree = ET.parse(filePath)
            root = tree.getroot()
                
            namespace = {
                "": "http://www.topografix.com/GPX/1/1",
                "gpxtpx": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1"
            }

            track_points = []
            for trkpt in root.findall(".//trkpt", namespace):
                lat = trkpt.get("lat")
                lon = trkpt.get("lon")
                ele = float(trkpt.find("ele", namespace).text)
                time = trkpt.find("time", namespace).text

                # Extension - heart_rate
                hr = None
                extensions = trkpt.find("extensions", namespace)

                if extensions is not None:
                    hr_elem = extensions.find("gpxtpx:TrackPointExtension/gpxtpx:hr", namespace)
                    if hr_elem is not None:
                        hr = hr_elem

                tp = GPX.__TrackPoint(lat, lon, ele, time, hr)
                track_points.append(tp)

            data = {
                "Latitude": [tp.lat for tp in track_points],
                "Longitude": [tp.lon for tp in track_points],
                "Elevation": [tp.ele for tp in track_points],
                "Time": [tp.time for tp in track_points],
                "HeartRate": [tp.hr for tp in track_points]
            }
            self.track_df = pd.DataFrame(data)

            self.track_df["Time"] = pd.to_datetime(self.track_df["Time"])
        
            self.__v_min_elevation = self.track_df["Elevation"].astype(float).min()
            self.__v_max_elevation = self.track_df["Elevation"].astype(float).max()    
            self.__v_duration = self.track_df["Time"].max() - self.track_df["Time"].min()
            
            exerciseInfo = root.find("exerciseinfo", namespace)
            if exerciseInfo != None:
                self.__v_total_distance = float(exerciseInfo.find("distance", namespace).text)
            else:
                self.__TotalDistance()
        
        except ET.ParseError as e:
            raise Exception(f"Failed to parse GPX file: {e}")
        except FileNotFoundError:
            raise Exception(f"The file {filePath} does not exist.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {e}")
    
    # --- Public Functions -----------------------
    def __init__(self, filePath):
        self.__ReadFile(filePath)

    def GetDistance(self):
        return self.__v_total_distance

    def GetMinElevation(self):
        return self.__v_min_elevation

    def GetMaxElevation(self):
        return self.__v_max_elevation

    def GetDuration(self):
        return self.__v_duration

