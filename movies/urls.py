from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path("search/", views.movie_search, name="movie_search"),
    path("movie/<int:tmdb_id>/", views.movie_detail, name="movie_detail"),
]