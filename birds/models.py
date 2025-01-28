from django.db import models


class Habitat(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Bird(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    habitat = models.ForeignKey(
        Habitat,
        on_delete=models.CASCADE,
        related_name="birds",
        null=True,
        blank=True
    )
    background = models.TextField()
    population_trend = models.CharField(
        max_length=100,
        choices=[
            ('increasing', 'Increasing'),
            ('decreasing', 'Decreasing'),
            ('stable', 'Stable')
        ]
        , blank=True, null=True
    )
    upper_elevation_limit = models.PositiveIntegerField(null=True, blank=True)
    lower_elevation_limit = models.PositiveIntegerField(null=True, blank=True)
    url = models.URLField()

    
    def __str__(self):
        return self.name

class Birdset(models.Model):
    bird = models.ForeignKey(
        Bird,
        on_delete=models.CASCADE,
        related_name="birdsets"  # Changed from "birds" to "birdsets"
    )

    image = models.ImageField(upload_to="images/")
    audio = models.FileField(upload_to="audio/", blank=True, null=True)

    def __str__(self):
        return self.bird.name

