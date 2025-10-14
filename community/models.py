from django.db import models
from django.contrib.auth.models import User
from movies.models import Review


class ReviewLike(models.Model):
    """
    Model representing a 'like' given by a user to a movie review.

    Attributes:
        user (User): The user who liked the review.
        review (Review): The review that was liked.
        created_at (datetime): The date and time when the like was created.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name="reviewlike_set"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')

    def __str__(self):
        """
        Returns a string representation of the ReviewLike instance.
        """
        return (
            f"{self.user.username} liked review {self.review.id}"
        )
