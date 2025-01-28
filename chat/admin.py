from django.contrib import admin
from .models import BirdContent, BirdChat

@admin.register(BirdChat)
class BirdChatAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BirdChat._meta.fields]
    search_fields = ('species_name',)

@admin.register(BirdContent)
class BirdContextAdmin(admin.ModelAdmin):
    list_display = [field.name for field in BirdContent._meta.fields]
    search_fields = ('bird','content','embedding',)