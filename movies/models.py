from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    """
    Represents a movie with details such as title, description, release year,
    poster, and TMDB information.
    """
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_year = models.PositiveIntegerField(null=True, blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    tmdb_id = models.IntegerField(unique=True, null=True, blank=True)
    release_date = models.CharField(max_length=20, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    poster_path = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    """
    Represents a review for a movie, including rating, comment,
    moderation fields, and user association.
    """
    RATING_CHOICES = [(i, '⭐' * i) for i in range(1, 6)]

    movie = models.ForeignKey(
        "Movie",
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')

    def __str__(self):
        return f"{self.movie.title} - {self.user.username} ({self.rating})"


class Watchlist(models.Model):
    """
    Represents a user's watchlist entry for a movie, including watched status.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watchlist"
    )
    movie = models.ForeignKey(
        "Movie",
        on_delete=models.CASCADE,
        related_name="watchlist_entries"
    )
    watched = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        status = 'Watched' if self.watched else 'Unwatched'
        return (
            f"{self.user.username} - {self.movie.title} ({status})"
        )