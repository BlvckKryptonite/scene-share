from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from ..models import Movie, Review
from ..forms import ReviewForm

# Create your tests here.


class TestMovieViews(TestCase):
    """
    Test suite for movie-related views and forms.
    Covers:
    - Rendering of the movie detail page.
    - Posting valid and invalid movie reviews.
    """

    def setUp(self):
        """
        Create a user and a sample movie for testing.
        """
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.movie = Movie.objects.create(
            title="Inception",
            tmdb_id=12345,
            overview="A mind-bending thriller."
        )

    def test_movie_detail_get(self):
        """
        Test that the movie detail page renders successfully
        and includes the correct movie data and review form.
        """
        response = self.client.get(reverse('movie_detail',
                                           args=[self.movie.tmdb_id]))

        # Ensure the page loads successfully
        self.assertEqual(response.status_code, 200)

        # Verify the movie title appears on the page
        self.assertIn(b"Inception", response.content)

        # Verify the review form is in the context
        self.assertIsInstance(response.context['review_form'], ReviewForm)

    def test_movie_review_post_valid(self):
        """
        Test submitting a valid review for a movie as an authenticated user.
        """
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse('add_review', args=[self.movie.id]),  # Using local DB id
            {
                "rating": 5,
                "body": "Absolutely loved it!"
            }
        )

        # Expect a redirect after successful submission
        self.assertEqual(response.status_code, 302)

        # Verify the review was created in the database
        self.assertTrue(Review.objects.filter(
            movie=self.movie, user=self.user).exists())

    def test_movie_review_post_invalid(self):
        """
        Test submitting an invalid (empty) review form.
        The form should re-render instead of redirecting.
        """
        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(
            reverse('add_review', args=[self.movie.id]),  # Local DB id
            {
                "rating": "",  # Invalid rating
                "body": ""     # Empty body
            }
        )

        # Form should re-render with validation errors
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'rating',
                             'This field is required.')
