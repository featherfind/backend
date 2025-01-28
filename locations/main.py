import math
from datetime import datetime, timedelta
import json
from.data import bird_data

# Function to calculate the next location based on bearing and distance
def calculate_next_location(lat, lon, bearing, distance):
    R = 6371000  # Radius of Earth in meters
    lat, lon, bearing = map(math.radians, [lat, lon, bearing])

    # Calculate the new latitude
    new_lat = math.asin(
        math.sin(lat) * math.cos(distance / R) +
        math.cos(lat) * math.sin(distance / R) * math.cos(bearing)
    )

    # Calculate the new longitude
    new_lon = lon + math.atan2(
        math.sin(bearing) * math.sin(distance / R) * math.cos(lat),
        math.cos(distance / R) - math.sin(lat) * math.sin(new_lat)
    )

    # Convert back to degrees
    new_lat, new_lon = map(math.degrees, [new_lat, new_lon])
    return new_lat, new_lon

# Function to calculate the bearing between two points
def calculate_bearing(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360  # Normalize to 0-360
    return compass_bearing

# Function to calculate distance between two points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Radius of Earth in meters
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Main function to predict future location and timestamp
def predict_future_location(bird_data, future_distance=1000):
    for bird in bird_data:
        # Get the last two points
        last_point = bird["data"][-1]
        second_last_point = bird["data"][-2]

        # Calculate bearing
        bearing = calculate_bearing(
            second_last_point["latitude"], second_last_point["longitude"],
            last_point["latitude"], last_point["longitude"]
        )

        # Calculate distance between the last two points
        distance = haversine(
            second_last_point["latitude"], second_last_point["longitude"],
            last_point["latitude"], last_point["longitude"]
        )

        # Calculate time difference (in seconds)
        last_timestamp = datetime.strptime(last_point["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
        second_last_timestamp = datetime.strptime(second_last_point["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ")
        time_difference = (last_timestamp - second_last_timestamp).total_seconds()

        # Calculate speed (meters per second)
        speed = distance / time_difference if time_difference > 0 else 0

        # Predict time to cover future_distance
        if speed > 0:
            time_to_next_location = future_distance / speed
        else:
            time_to_next_location = 0

        # Predict timestamp
        predicted_timestamp = last_timestamp + timedelta(seconds=time_to_next_location)

        # Predict next location
        predicted_lat, predicted_lon = calculate_next_location(
            last_point["latitude"], last_point["longitude"], bearing, future_distance
        )

        # Append the predicted point to the bird's data
        bird["data"].append({
            "latitude": predicted_lat,
            "longitude": predicted_lon,
            "timestamp": predicted_timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        })

    return bird_data

# Predict future location and timestamp
future_distance = 1000  # Distance in meters
updated_bird_data = predict_future_location(bird_data, future_distance)

# Output the updated JSON
print(json.dumps(updated_bird_data, indent=4))

