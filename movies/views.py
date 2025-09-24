from django.shortcuts import render
from .models import Movie, Review
from .forms import ReviewForm

# Create your views here.
def home(request):
    movies = Movie.objects.all()

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
        form = ReviewForm()

    context = {
        'movies': movies,
        'form': form,
    }

    return render(request, 'movies/home.html', context)