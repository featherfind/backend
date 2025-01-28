from rest_framework import serializers
from .models import Bird, Birdset, Habitat


class HabitatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habitat
        fields = "__all__"

class BirdsetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Birdset
        fields = ['id', 'bird', 'image', 'audio']

class BirdSerializer(serializers.ModelSerializer):
    birdsets = BirdsetSerializer(many=True, read_only=True)
    
    class Meta:
        model = Bird
        fields = ['id', 'name', 'species', 'habitat', 'background', 
                 'population_trend', 'upper_elevation_limit', 
                 'lower_elevation_limit', 'url', 'birdsets']

