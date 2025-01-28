from datetime import datetime
from django.utils.timezone import make_aware
from ..birds.models import Bird
from .models import BirdLocation, Location


def bird_data():
    # Initialize the list that will hold the final data
    bird_datas = []

    # Get all birds from the Bird model
    birds = Bird.objects.all()

    for bird in birds:
        bird_info = {
            "label": bird.label,
            "data": []
        }

        # Get all BirdLocation instances related to the current bird
        bird_locations = BirdLocation.objects.filter(bird=bird).select_related('location')

        for bird_location in bird_locations:
            location = bird_location.location
            timestamp = bird_location.spotted_time

            # Structure the data as required: latitude, longitude, timestamp
            bird_info["data"].append({
                "latitude": location.latitude,
                "longitude": location.longitude,
                "timestamp": make_aware(timestamp).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            })

        # Append this bird's information to the final bird_data list
        bird_datas.append(bird_info)

    return bird_datas