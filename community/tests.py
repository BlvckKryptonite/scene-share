from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from movies.models import Review, Movie
from community.models import ReviewLike

# Create your tests here.


class ReviewLikeTests(TestCase):
    """
    Test suite for the ReviewLike model and toggle_review_like view.
    """

    def setUp(self):
        """
        Create test users, a movie, a review, and initialize client.
        """
        self.client = Client()

        # Test users
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.other_user = User.objects.create_user(
            username="reviewer", password="password123"
        )

        # Trest movie
        self.movie = Movie.objects.create(title="Test Movie")

        # Review test
        self.review = Review.objects.create(
            user=self.other_user,
            movie=self.movie,
            comment="Damn, what a great movie!",  # Corrected field name
            rating=5
        )

        # URL for toggling review like
        self.like_url = reverse("toggle_review_like", args=[self.review.id])

    def test_str_representation(self):
        """
        Test that the string representation of ReviewLike is correct.
        """
        like = ReviewLike.objects.create(user=self.user, review=self.review)
        self.assertEqual(
            str(like), f"{self.user.username} liked review {self.review.id}"
        )

    def test_like_toggle_requires_login(self):
        """
        Test that unauthenticated users cannot like a review.
        """
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith("/accounts/login/"))

    def test_like_and_unlike_review(self):
        """
        Test toggling a like: first adds it, second removes it.
        """
        self.client.login(username="testuser", password="password123")

        # First POST - adds like
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["liked"])
        self.assertEqual(data["like_count"], 1)
        self.assertTrue(ReviewLike.objects.filter(
            user=self.user, review=self.review
        ).exists())

        # Second POST -- removes like
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data["liked"])
        self.assertEqual(data["like_count"], 0)
        self.assertFalse(ReviewLike.objects.filter(
            user=self.user, review=self.review
        ).exists())

    def test_invalid_request_method(self):
        """
        Test that a non-POST request returns an error.
        """
        self.client.login(username="testuser", password="password123")
        response = self.client.get(self.like_url)
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())
