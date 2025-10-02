from django.contrib import admin
from django.utils.html import format_html
from .models import Movie, Review

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "get_release_year", "get_poster_thumb")
    search_fields = ("title",)

    def get_release_year(self, obj):
        if obj.release_year:
            return obj.release_year
        elif obj.release_date:
            return obj.release_date[:4]  # extract YYYY
        return None
    get_release_year.short_description = "Release Year"

    def get_poster_thumb(self, obj):
        if obj.poster:
            return format_html('<img src="{}" width="60" />', obj.poster.url)
        elif obj.poster_path:
            return format_html('<img src="https://image.tmdb.org/t/p/w200{}" width="60" />', obj.poster_path)
        return "No Poster"
    get_poster_thumb.short_description = "Poster"

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("movie", "user", "rating", "created_at")
    search_fields = ("movie__title", "user__username")
