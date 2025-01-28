from django.contrib import admin
from .models import Location, BirdLocation

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Location._meta.fields]
    search_fields = ("name", "longitude", "latitude")

@admin.register(BirdLocation)
class BirdLocationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BirdLocation._meta.fields]
    search_fields = ("name", "bird")