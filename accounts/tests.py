from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

# Create your tests here.


class ProfileModelTests(TestCase):
    """Tests for the Profile model."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123")

    def test_profile_created_on_user_creation(self):
        """Test that a profile is automatically created for a new user."""
        self.assertTrue(hasattr(self.user, "profile"))
        self.assertEqual(str(self.user.profile), "testuser's profile")

    def test_profile_str_method(self):
        """Test the __str__ method of Profile model."""
        profile = self.user.profile
        self.assertEqual(str(profile), f"{self.user.username}'s profile")


class RegisterViewTests(TestCase):
    """Tests for the register view."""

    def setUp(self):
        self.client = Client()

    def test_register_view_get(self):
        """Test that the register page renders correctly."""
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_valid_registration_creates_user(self):
        """Test that a valid registration
        creates a new user and redirects to login."""
        data = {
            "username": "newuser",
            "email": "newuser@example.com",  # Required email
            "password1": "StrongPass!234",
            "password2": "StrongPass!234",
        }
        response = self.client.post(reverse("register"), data, follow=True)

        # Debug output (in case form still fails)
        if response.context and "form" in response.context:
            errors = response.context["form"].errors
            if errors:
                print("Form errors:", errors)

        # Check user creation
        self.assertTrue(User.objects.filter(username="newuser").exists())

        # Check for success message
        messages = list(response.context["messages"])
        self.assertTrue(any("Account created" in str(msg) for msg in messages))

        # Confirm redirect chain includes login
        self.assertTrue(any(
            "login" in url for url, _ in response.redirect_chain))


class ProfileViewTests(TestCase):
    """Tests for the profile view."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123")
        self.client = Client()
        self.client.login(username="testuser", password="password123")

    def test_profile_page_loads(self):
        """Test that the profile page loads for logged-in users."""
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/profile.html")

    def test_profile_update(self):
        """Test that a user can update their profile and username."""
        data = {"username": "updateduser", "bio": "New bio here!"}
        response = self.client.post(reverse("profile"), data, follow=True)

        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")
        self.assertEqual(self.user.profile.bio, "New bio here!")

        messages = list(response.context["messages"])
        self.assertTrue(any(
            "updated successfully" in str(msg) for msg in messages))
