from django.urls import path
from . import views

urlpatterns = [
    path("like/<int:review_id>/", views.toggle_review_like,
         name="toggle_review_like"),
]
