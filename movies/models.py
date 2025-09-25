from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    release_year = models.PositiveIntegerField(null=True, blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)

    def __str__(self):
        return self.title


# The Review model
class Review(models.Model):
    RATING_CHOICES = [(i, '⭐' * i) for i in range(1, 6)]

    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')  # Each user can only review once

    def __str__(self):
        return f"{self.movie.title} - {self.user.username} ({self.rating})"


"""
class Review(models.Model):
    RATING_CHOICES = [(i, '⭐' * i) for i in range(1, 6)]

    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="reviews")"""