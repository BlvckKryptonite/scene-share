from django.contrib import admin
from .models import Movie, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "get_release_year", "get_poster")
    search_fields = ("title",)

    def get_release_year(self, obj):
        if obj.release_date:
            return obj.release_date.split("-")[0]  # Extract year from YYYY-MM-DD
        return None
    get_release_year.short_description = "Release Year"

    def get_poster(self, obj):
        if obj.poster_path:
            return f"https://image.tmdb.org/t/p/w200{obj.poster_path}"
        return None
    get_poster.short_description = "Poster"

# Reviews
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "rating", "created_at")
    search_fields = ("movie__title", "user__username")
