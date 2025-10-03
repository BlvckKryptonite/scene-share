from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path("search/", views.movie_search, name="movie_search"),
    path("movie/<int:tmdb_id>/", views.movie_detail, name="movie_detail"),
    path("movie/<int:movie_id>/review/", views.add_review, name="add_review"),

    # Watchlist URLs — support both tmdb_id and local movie_id
    path('watchlist/add/tmdb/<int:tmdb_id>/', views.add_to_watchlist, name='add_to_watchlist_tmdb'),
    path('watchlist/add/local/<int:movie_id>/', views.add_to_watchlist, name='add_to_watchlist_local'),

    path('watchlist/remove/tmdb/<int:tmdb_id>/', views.remove_from_watchlist, name='remove_from_watchlist_tmdb'),
    path('watchlist/remove/local/<int:movie_id>/', views.remove_from_watchlist, name='remove_from_watchlist_local'),

    path('watchlist/toggle/tmdb/<int:tmdb_id>/', views.toggle_watched, name='toggle_watched_tmdb'),
    path('watchlist/toggle/local/<int:movie_id>/', views.toggle_watched, name='toggle_watched_local'),

    path("watchlist/", views.watchlist, name="watchlist"),
]
