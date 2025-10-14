from django.contrib import admin
from django.contrib.admin.models import LogEntry, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str
from django.utils.html import format_html
from .models import Movie, Review


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Admin interface for the Movie model.
    Displays movie title, release year, and poster thumbnail.
    Allows searching by title.
    """
    list_display = ("title", "get_release_year", "get_poster_thumb")
    search_fields = ("title",)

    def get_release_year(self, obj):
        if obj.release_year:
            return obj.release_year
        elif obj.release_date:
            return obj.release_date[:4]  # extract year
        return None
    get_release_year.short_description = "Release Year"

    def get_poster_thumb(self, obj):
        """
        Returns an HTML image tag for the movie's poster thumbnail.
        Uses local poster if available, otherwise uses external poster path.
        """
        if obj.poster:
            return format_html(
                '<img src="{}" width="60" />', obj.poster.url
            )
        elif obj.poster_path:
            return format_html(
                '<img src="https://image.tmdb.org/t/p/w200{}" width="60" />',
                obj.poster_path
            )
        return "No Poster"
    get_poster_thumb.short_description = "Poster"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for the Review model.
    Displays review details and provides bulk actions for approving,
    flagging, and unflagging reviews, with logging for each action.
    """
    list_display = (
        "movie", "user", "rating", "approved", "flagged", "created_at"
    )
    search_fields = ("movie__title", "user__username", "comment")
    list_filter = ("approved", "flagged", "rating", "created_at")
    actions = ["approve_reviews", "flag_reviews", "unflag_reviews"]

    def get_content_type_id(self):
        """
        Returns the content type ID for the Review model.
        """
        return ContentType.objects.get_for_model(self.model).pk

    def approve_reviews(self, request, queryset):
        """
        Bulk action to approve selected reviews and unflag them.
        Logs each approval action.
        """
        updated = queryset.update(approved=True, flagged=False)
        content_type_id = self.get_content_type_id()
        for review in queryset:
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=content_type_id,
                object_id=review.id,
                object_repr=force_str(review),
                action_flag=CHANGE,
                change_message=f"Approved review: {review.id}",
            )
        self.message_user(request, f"{updated} review(s) approved.")
    approve_reviews.short_description = "✅ Approve selected reviews"

    def flag_reviews(self, request, queryset):
        updated = queryset.update(flagged=True)
        content_type_id = self.get_content_type_id()
        for review in queryset:
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=content_type_id,
                object_id=review.id,
                object_repr=force_str(review),
                action_flag=CHANGE,
                change_message=(
                    f"Flagged review for moderation: {review.id}"
                ),
            )
        self.message_user(
            request, f"{updated} review(s) flagged for review."
        )
    flag_reviews.short_description = "🚩 Flag selected reviews"

    def unflag_reviews(self, request, queryset):
        updated = queryset.update(flagged=False)
        content_type_id = self.get_content_type_id()
        for review in queryset:
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=content_type_id,
                object_id=review.id,
                object_repr=force_str(review),
                action_flag=CHANGE,
                change_message=f"Unflagged review: {review.id}",
            )
        self.message_user(request, f"{updated} review(s) unflagged.")
    unflag_reviews.short_description = "❎ Unflag selected reviews"

    def delete_queryset(self, request, queryset):
        """
        Logs each review deletion before performing the bulk delete.
        """
        content_type_id = self.get_content_type_id()
        for review in queryset:
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=content_type_id,
                object_id=review.id,
                object_repr=force_str(review),
                action_flag=DELETION,
                change_message=f"Deleted review: {review.id}",
            )
        super().delete_queryset(request, queryset)