from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from .models import Movie, Review
from .forms import ReviewForm

def home(request):
    # Annotate movies with their average rating
    movies = Movie.objects.all().annotate(avg_rating=Avg('reviews__rating'))

    # Initialize a dict of forms for all movies
    forms_dict = {movie.id: ReviewForm() for movie in movies}

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        movie_id = request.POST.get('movie_id')
        movie = get_object_or_404(Movie, pk=movie_id)

        if form.is_valid():
            # Create or update review for this user/movie
            Review.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={
                    'rating': form.cleaned_data['rating'],
                    'comment': form.cleaned_data['comment']
                }
            )
            return redirect('home')
        else:
            # Replace the form in forms_dict with the invalid one
            forms_dict[int(movie_id)] = form

    context = {
        'movies': movies,
        'forms_dict': forms_dict
    }

    return render(request, 'movies/home.html', context)

# EDIT reviews
def edit_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    # Only the review owner can edit
    if review.user != request.user:
        return redirect('home')

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'movies/edit_review.html', {'form': form, 'review': review})

# DELETE reviews
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)

    if review.user == request.user:
        review.delete()

    return redirect('home')