from django.db import models
from birds.models import Bird, Habitat


class Location(models.Model):
    '''
    Location for the deployed devices. (stations)
    '''
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=18, decimal_places=15) 
    longitude = models.DecimalField(max_digits=18, decimal_places=15)
    description = models.TextField(blank=True, null=True)
    altitude = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    habitat = models.ForeignKey(
        Habitat,
        on_delete=models.SET_NULL,  
        related_name="locations",    
        null=True,
        blank=True                   
    )
    place_type = models.CharField(
        max_length=50,
        choices = [
            ('Observation Site', "Observation Site"),
            ('Monitoring Station', 'Monitoring Station'),
            ('Protected Area', 'Protected Area'),
            ('National Park', 'National Park'),
            ('Forest', 'Forest'),
            ('Application', 'Application')
        ]
    )
    
    def __str__(self):
        return self.name

class BirdLocation(models.Model):
    '''
    Location for bird where they are recorded and mapped. (application)
    '''
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        null=True,
        related_name="bird_locations"
    )
    bird = models.ForeignKey(
        Bird, on_delete=models.CASCADE, 
        null=True, 
        related_name="bird")
    spotted_time = models.DateTimeField()

    def __str__(self):
        return self.location.name