from django.contrib import admin
from .models import Bird, Birdset, Habitat

@admin.register(Bird)
class BirdAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Bird._meta.fields]
    search_fields = ('name', 'species')

@admin.register(Birdset)
class BirdsetAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Birdset._meta.fields]
    search_fields = ('name',)

@admin.register(Habitat)
class HabitatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Habitat._meta.fields]
    search_fields = ('name',)