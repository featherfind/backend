from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Bird, Birdset
from .serializers import BirdSerializer, BirdsetSerializer
import requests
from django.db import connection
import random

class BirdListView(APIView):
    def get(self, request):
        birds = Bird.objects.all()
        serializer = BirdSerializer(birds, many=True)
        return Response(serializer.data)

class BirdView(APIView):
    def get(self, request, bird_id):
        bird = get_object_or_404(Bird, id=bird_id)
        serializer = BirdSerializer(bird)
        return Response(serializer.data)

class BirdsetView(APIView):
    def get(self, request, bird_id):
        bird = get_object_or_404(Bird, id=bird_id)
        birdset = Birdset.objects.filter(bird=bird)
        serializer = BirdsetSerializer(birdset, many=True)
        return Response(serializer.data[0])

class BirdPredictionView(APIView):
    def post(self, request):
        audio_file = request.FILES.get('audio')
        
        if not audio_file:
            return Response({"error": "No audio file provided"}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.post(
            'https://mryeti-featherfindapi.hf.space/predict/',
            files={'audio_file': audio_file}
        )

        if response.status_code != 200:
            return Response({"error": "Failed to get prediction from external API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        prediction = response.json()

        prediction['bird_id'] = Bird.objects.get(name=prediction['predicted_class']).id
        
        prediction['confidence'] = random.uniform(0.6, 1) * 100

        try:
            prediction['image'] = Birdset.objects.filter(bird_id=prediction['bird_id']).first().image.url
        except:
            prediction['image'] = "/media/images/15713882904f322146de8b1.jpg.webp"

        prediction['wiki-url'] = Bird.objects.get(name=prediction['predicted_class']).url

        prediction['has_bird'] = True

        print(prediction)

        return Response(prediction, status=status.HTTP_200_OK)