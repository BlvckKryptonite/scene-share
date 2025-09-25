from django.shortcuts import render, redirect
from .models import Movie, Review
from .forms import ReviewForm

# Create your views here.
def home(request):
    movies = Movie.objects.all()

    # Initialize a dict of forms for all movies
    forms_dict = {movie.id: ReviewForm() for movie in movies}

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            movie_id = request.POST.get('movie_id') # hidden input in form
            review.movie = Movie.objects.get(pk=movie_id)
            review.save()
            return redirect('home')
        else:
            # Replace the form for the movie that failed validation
            movie_id = int(request.POST.get('movie_id'))
            forms_dict[movie_id] = form

    context = {
        'movies': movies,
        'forms_dict': forms_dict,  # Always pass the dict to template
    }

    return render(request, 'movies/home.html', context)