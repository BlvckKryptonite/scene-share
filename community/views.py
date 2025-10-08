from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from movies.models import Review
from .models import ReviewLike

# Create your views here.
@login_required
def toggle_review_like(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    like, created = ReviewLike.objects.get_or_create(user=request.user, review=review)

    # toggle like/unlike
    if not created:
        like.delete()

    # Redirect back to the same page the user was on
    return redirect(request.META.get('HTTP_REFERER', 'home'))
