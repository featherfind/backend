from rest_framework import serializers
from .models import Location, BirdLocation
from birds.serializers import BirdSerializer, HabitatSerializer

class LocationSerializer(serializers.ModelSerializer):
    habitat = HabitatSerializer(read_only=True)
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'latitude', 'longitude', 'description', 
                 'altitude', 'habitat', 'place_type']

class BirdLocationSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    bird = BirdSerializer(read_only=True)
    
    class Meta:
        model = BirdLocation
        fields = ['id', 'location', 'bird', 'spotted_time']