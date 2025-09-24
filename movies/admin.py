from django.contrib import admin
from .models import Movie, Review

# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year')
    search_fields = ('title',)

# Reviews
admin.site.register(Review)