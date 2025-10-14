from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from movies.models import Review
from .models import ReviewLike


@login_required
def toggle_review_like(request, review_id):
    """
    Toggle the like status for a review by the current user.

    If the user has already liked the review, the like is removed.
    Otherwise, a like is added. Returns a JSON response with the
    current like status and total like count for the review.
    """
    if request.method == "POST":
        review = get_object_or_404(Review, id=review_id)
        existing_like = ReviewLike.objects.filter(
            user=request.user, review=review
        )

        if existing_like.exists():
            existing_like.delete()
            liked = False
        else:
            ReviewLike.objects.create(user=request.user, review=review)
            liked = True

        like_count = ReviewLike.objects.filter(review=review).count()

        return JsonResponse({
            "liked": liked,
            "like_count": like_count
        })

    return JsonResponse({"error": "Invalid request"}, status=400)
