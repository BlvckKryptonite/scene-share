"""
Tests to ensure that all URLs in this app app correctly resolve
to their intended view functions. These tests verify both static and
parameterized routes.
"""

from django.test import SimpleTestCase
from django.urls import reverse, resolve
from movies import views


class TestMovieURLs(SimpleTestCase):
    """Test suite for verifying URL patterns in the movies app."""

    def test_home_url_resolves(self):
        """Ensure the home page URL resolves to the home view."""
        url = reverse('home')
        self.assertEqual(resolve(url).func, views.home)

    def test_movie_detail_url_resolves(self):
        """Ensure the movie detail URL
        resolves correctly with a tmdb_id."""
        url = reverse('movie_detail', args=[123])
        self.assertEqual(resolve(url).func, views.movie_detail)

    def test_add_review_url_resolves(self):
        """Ensure the add review URL
        resolves correctly with a movie_id."""
        url = reverse('add_review', args=[1])
        self.assertEqual(resolve(url).func, views.add_review)

    def test_edit_review_url_resolves(self):
        """Ensure the edit review URL
        resolves correctly with a review_id."""
        url = reverse('edit_review', args=[5])
        self.assertEqual(resolve(url).func, views.edit_review)

    def test_delete_review_url_resolves(self):
        """Ensure the delete review URL
        resolves correctly with a review_id."""
        url = reverse('delete_review', args=[7])
        self.assertEqual(resolve(url).func, views.delete_review)

    def test_movie_search_url_resolves(self):
        """Ensure the movie search URL resolves correctly."""
        url = reverse('movie_search')
        self.assertEqual(resolve(url).func, views.movie_search)

    def test_watchlist_urls_resolve(self):
        """Ensure all watchlist URLs
        (add, remove, toggle, list) resolve correctly."""
        tmdb_add = reverse('add_to_watchlist_tmdb', args=[101])
        local_add = reverse('add_to_watchlist_local', args=[10])
        tmdb_remove = reverse('remove_from_watchlist_tmdb', args=[202])
        local_remove = reverse('remove_from_watchlist_local', args=[20])
        tmdb_toggle = reverse('toggle_watched_tmdb', args=[303])
        local_toggle = reverse('toggle_watched_local', args=[30])
        watchlist = reverse('watchlist')

        self.assertEqual(resolve(tmdb_add).func, views.add_to_watchlist)
        self.assertEqual(resolve(local_add).func, views.add_to_watchlist)
        self.assertEqual(
            resolve(tmdb_remove).func, views.remove_from_watchlist)
        self.assertEqual(
            resolve(local_remove).func, views.remove_from_watchlist)
        self.assertEqual(resolve(tmdb_toggle).func, views.toggle_watched)
        self.assertEqual(resolve(local_toggle).func, views.toggle_watched)
        self.assertEqual(resolve(watchlist).func, views.watchlist)
