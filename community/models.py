from django.db import models
from django.contrib.auth.models import User
from movies.models import Review 
from django.utils import timezone # For review tiem posted.

# Create your models here.
class ReviewLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_likes")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        return f"{self.user.username} liked {self.review}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.review}"