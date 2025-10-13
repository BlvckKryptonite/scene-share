from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Movie, Review, Watchlist
from .forms import ReviewForm
from django.conf import settings
import requests
from community.models import ReviewLike 

def home(request):
    # Annotate movies with their average rating
    movies = Movie.objects.all().annotate(avg_rating=Avg('reviews__rating'))

    # Initialize a dict of forms for all movies
    forms_dict = {movie.id: ReviewForm() for movie in movies}

    # Track which movies the current user has in watchlist & watched status
    watchlist_movie_ids = []
    watch_status = {}
    if request.user.is_authenticated:
        entries = request.user.watchlist.all()
        watchlist_movie_ids = [entry.movie.id for entry in entries]
        watch_status = {entry.movie.id: entry.watched for entry in entries}

    # New or updated review submission
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        movie_id = request.POST.get('movie_id')
        movie = get_object_or_404(Movie, pk=movie_id)

        if form.is_valid():
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
            forms_dict[int(movie_id)] = form

    # Add "is_liked" flag for each review (only approved ones)
    if request.user.is_authenticated:
        reviews = Review.objects.filter(is_approved=True).select_related('user', 'movie').prefetch_related('reviewlike_set')
        for review in reviews:
            review.is_liked = review.reviewlike_set.filter(user=request.user).exists()
    else:
        reviews = Review.objects.filter(is_approved=True).select_related('user', 'movie')
    for review in reviews:
        review.is_liked = False

    context = {
        'movies': movies,
        'forms_dict': forms_dict,
        'watchlist_movie_ids': watchlist_movie_ids,
        'watch_status': watch_status,
        'reviews': reviews, 
    }

    return render(request, 'movies/home.html', context)

# EDIT reviews
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            # Redirect to movie detail if review belongs to an API-fetched movie
            if review.movie.tmdb_id:
                return redirect('movie_detail', tmdb_id=review.movie.tmdb_id)
            return redirect('home')
    else:
        form = ReviewForm(instance=review)

    return render(request, 'movies/edit_review.html', {'form': form, 'review': review})

# DELETE reviews
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if review.user != request.user:
        raise PermissionDenied

    movie = review.movie
    review.delete()
    # Redirect to movie detail if review belongs to an API-fetched movie
    if movie.tmdb_id:
        return redirect('movie_detail', tmdb_id=movie.tmdb_id)
    return redirect('home')


# Movie search view
def movie_search(request):
    query = request.GET.get("q")
    results = []
    error_message = None

    # Check if API key is set
    api_key = getattr(settings, "TMDB_API_KEY", None)
    if not api_key:
        error_message = "Movie search is currently unavailable (API key missing)."
        return render(request, "movies/search.html", {"results": results, "query": query, "error_message": error_message})

    if query:
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": api_key,
            "query": query,
            "language": "en-US",
            "include_adult": True,
        }

        try:
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                results = data.get("results", [])
                if not results:
                    error_message = f"No movies found for '{query}'."
            elif response.status_code == 401:
                error_message = "Movie search is currently unavailable (invalid API key)."
            else:
                error_message = f"TMDb API returned status code {response.status_code}"

        except requests.exceptions.RequestException as e:
            error_message = f"Error contacting TMDb API: {e}"

    return render(
        request,
        "movies/search.html",
        {
            "results": results,
            "query": query,
            "error_message": error_message,
        },
    )


# Movie details view
def movie_detail(request, tmdb_id):
    # Try to get the movie locally
    movie, created = Movie.objects.get_or_create(tmdb_id=tmdb_id)

    # If newly created, fetch details from TMDb
    if created:
        url = f"https://api.themoviedb.org/3/movie/{tmdb_id}"
        params = {"api_key": settings.TMDB_API_KEY, "language": "en-US"}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            movie.title = data.get("title")
            movie.release_date = data.get("release_date")
            movie.overview = data.get("overview")
            movie.poster_path = data.get("poster_path")
            movie.save()
        else:
            # Fallback if TMDb fails
            movie.title = "Unknown Title"
            movie.overview = "No details available."
            movie.save()

    # Fetch only approved reviews
    reviews = Review.objects.filter(movie=movie, approved=True).order_by("-id")

    # Determine if user already has this movie in watchlist
    watchlist_movies = []
    if request.user.is_authenticated:
        watchlist_movies = request.user.watchlist.values_list('movie__tmdb_id', flat=True)

    context = {
        "movie": movie,
        "reviews": reviews,
        "watchlist_movies": watchlist_movies,
    }
    return render(request, "movies/detail.html", context)


# API movies review submission form
@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            return redirect("movie_detail", tmdb_id=movie.tmdb_id)
    else:
        form = ReviewForm()
    return render(request, "movies/detail.html", {"movie": movie, "form": form})

# Add to watchlist view
@login_required
def add_to_watchlist(request, tmdb_id=None, movie_id=None):
    if not request.user.is_authenticated:
        return redirect('home')

    movie = get_object_or_404(Movie, tmdb_id=tmdb_id) if tmdb_id else get_object_or_404(Movie, id=movie_id)
    Watchlist.objects.get_or_create(user=request.user, movie=movie)
    return redirect('home')

# Remove from watchlist view
@login_required
def remove_from_watchlist(request, tmdb_id=None, movie_id=None):
    if not request.user.is_authenticated:
        return redirect('home')

    movie = get_object_or_404(Movie, tmdb_id=tmdb_id) if tmdb_id else get_object_or_404(Movie, id=movie_id)
    Watchlist.objects.filter(user=request.user, movie=movie).delete()

    # Redirect user back to referring page or fallback to home
    next_url = request.META.get('HTTP_REFERER', None)
    if next_url:
        return redirect(next_url)
    return redirect('home')

# Toggle watched/unwatched
@login_required
def toggle_watched(request, tmdb_id=None, movie_id=None):
    if not request.user.is_authenticated:
        return redirect('home')

    movie = get_object_or_404(Movie, tmdb_id=tmdb_id) if tmdb_id else get_object_or_404(Movie, id=movie_id)
    watch_entry = get_object_or_404(Watchlist, user=request.user, movie=movie)
    watch_entry.watched = not watch_entry.watched
    watch_entry.save()

    # Redirect back to where user came from, fallback to home
    return redirect(request.META.get('HTTP_REFERER', 'home'))

# The WATCHLIST view
@login_required
def watchlist(request):
    # Get all Watchlist entries for the current user
    entries = request.user.watchlist.select_related('movie').all()

    context = {
        'entries': entries
    }
    return render(request, 'movies/watchlist.html', context)

# MY Watchlist view so users can access see it
@login_required
def my_watchlist(request):
    return render(request, "movies/watchlist.html")