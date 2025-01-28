from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Location, BirdLocation
from .serializers import LocationSerializer, BirdLocationSerializer
from birds.models import Bird

class LocationListView(APIView):
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

class LocationView(APIView):
    def get(self, request, location_id):
        location = get_object_or_404(Location, id=location_id)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

class BirdLocationListView(APIView):
    def get(self, request):
        bird_locations = BirdLocation.objects.all()
        serializer = BirdLocationSerializer(bird_locations, many=True)
        return Response(serializer.data)

class BirdLocationView(APIView):
    def get(self, request, bird_id):
        bird = get_object_or_404(Bird, id=bird_id)
        bird_locations = BirdLocation.objects.filter(bird=bird)
        serializer = BirdLocationSerializer(bird_locations, many=True)
        return Response(serializer.data)
        
    def post(self, request, bird_id):
        latitude = request.data.get('latitude')
        longitude = request.data.get('longitude')
        timestamp = request.data.get('timestamp')
        location = Location.objects.create(latitude=latitude, longitude=longitude)
        bird = get_object_or_404(Bird, id=bird_id)
        bird_location = BirdLocation.objects.create(location=location, bird=bird, spotted_time=timestamp)
        serializer = BirdLocationSerializer(bird_location)
        return Response(serializer.data)

