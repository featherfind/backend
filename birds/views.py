from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Bird, Birdset
from .serializers import BirdSerializer, BirdsetSerializer
import requests
from django.db import connection
import random
from pydub import AudioSegment
import io
import platform


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
        
        audio = AudioSegment.from_file(io.BytesIO(audio_file.read()))
        mp3buffer = io.BytesIO()
        audio.export(mp3buffer, format='mp3')
        audio_file = mp3buffer.getvalue()

        bird_sound = self.get_bird_sound_prediction(audio_file)
        print(bird_sound)
        
        prediction = self.get_bird_prediction(audio_file)
        
        prediction['has_bird'] = True if bird_sound['has_bird'] else False

        return Response(prediction, status=status.HTTP_200_OK)

    def get_bird_sound_prediction(self, audio_file):
        if platform.system() == 'Darwin':
            import coremltools
            model = coremltools.models.MLModel('BirdML.mlmodel')
            output = model.predict({'audio_file': audio_file})
            return {'has_bird': output['target'] == 1}
        else:
            response = requests.post(
                'http://localhost:8765/predict/',
                files={'audio_file': audio_file}
            )
            if response.status_code != 200:
                raise Exception("Failed to get prediction from external API")
            return response.json()

    def get_bird_prediction(self, audio_file):
        response = requests.post(
            'https://mryeti-featherfindapi.hf.space/predict/',
            files={'audio_file': audio_file}
        )
        if response.status_code != 200:
            raise Exception("Failed to get prediction from external API")

        prediction = response.json()

        print(prediction)
        bird = Bird.objects.get(name=prediction['predicted_class'])
        prediction['bird_id'] = bird.id
        prediction['image'] = self.get_bird_image_url(bird.id)
        prediction['wiki-url'] = bird.url

        return prediction

    def get_bird_image_url(self, bird_id):
        birdset = Birdset.objects.filter(bird_id=bird_id).first()
        if birdset and birdset.image:
            return birdset.image.url
        return "/media/images/15713882904f322146de8b1.jpg.webp"

    def get_empty_prediction(self):
        return {
            'has_bird': False,
            'predicted_class': "",
            'confidence': 0,
            'bird_id': 0,
            'image': "",
            'wiki-url': ""
        }
