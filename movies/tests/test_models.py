from django.test import TestCase
from django.contrib.auth.models import User
from movies.models import Movie, Review, Watchlist


class TestMovieModels(TestCase):
    """Test suite for Movie, Review, and Watchlist models."""

    def setUp(self):
        """Create base user and movie for testing."""
        self.user = User.objects.create_user(
            username="testuser", password="testpass")
        self.movie = Movie.objects.create(
            title="Inception",
            description="A mind-bending thriller",
            release_year=2010,
            tmdb_id=12345,
            release_date="2010-07-16",
            overview="Dreams within dreams.",
            poster_path="/poster.jpg"
        )

    # --- Movie Model Tests ---
    def test_movie_str(self):
        """Test string representation of Movie model."""
        self.assertEqual(str(self.movie), "Inception")

    def test_movie_fields(self):
        """Ensure Movie fields are stored correctly."""
        self.assertEqual(self.movie.release_year, 2010)
        self.assertEqual(self.movie.tmdb_id, 12345)
        self.assertIn("Dreams", self.movie.overview)

    # --- Review Model Tests ---
    def test_review_creation_and_str(self):
        """Test creation of a Review and its string representation."""
        review = Review.objects.create(
            movie=self.movie,
            user=self.user,
            rating=5,
            comment="Amazing movie!",
            approved=True
        )
        self.assertEqual(str(review), "Inception - testuser (5)")
        self.assertTrue(review.approved)
        self.assertFalse(review.flagged)

    def test_unique_review_constraint(self):
        """Ensure a user can review a movie only once."""
        Review.objects.create(movie=self.movie, user=self.user, rating=4)
        with self.assertRaises(Exception):
            Review.objects.create(movie=self.movie, user=self.user, rating=3)

    # --- Watchlist Model Tests ---
    def test_watchlist_str_and_status(self):
        """Test string representation of Watchlist model."""
        watchlist_item = Watchlist.objects.create(
            user=self.user, movie=self.movie, watched=False
        )
        self.assertIn("Unwatched", str(watchlist_item))
        watchlist_item.watched = True
        watchlist_item.save()
        self.assertIn("Watched", str(watchlist_item))

    def test_unique_watchlist_constraint(self):
        """Ensure the same user cannot add the same movie twice."""
        Watchlist.objects.create(user=self.user, movie=self.movie)
        with self.assertRaises(Exception):
            Watchlist.objects.create(user=self.user, movie=self.movie)
