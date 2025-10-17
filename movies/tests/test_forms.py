from django.test import TestCase
from movies.forms import ReviewForm


class TestReviewForm(TestCase):
    """
    Tests for the ReviewForm to ensure validation works correctly.
    """

    def test_valid_form(self):
        """Test that the form is valid when all
        required fields are filled correctly."""
        form_data = {"rating": 5, "comment": "A fantastic movie!"}
        form = ReviewForm(data=form_data)
        self.assertTrue(
            form.is_valid(), "Form should be valid with proper data")

    def test_invalid_form_missing_rating(self):
        """Test that the form is invalid if rating is missing."""
        form_data = {"comment": "Missing rating!"}
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid(),
                         "Form should be invalid without rating")
        self.assertIn("rating", form.errors)

    def test_invalid_form_invalid_rating(self):
        """Test that the form is invalid
        for ratings outside the allowed range."""
        form_data = {"rating": 6, "comment": "Invalid rating!"}
        form = ReviewForm(data=form_data)
        self.assertFalse(
            form.is_valid(), "Form should reject invalid rating values")

    def test_comment_optional(self):
        """Test that the comment field can be left blank."""
        form_data = {"rating": 4, "comment": ""}
        form = ReviewForm(data=form_data)
        self.assertTrue(
            form.is_valid(), "Form should allow an empty comment field")
