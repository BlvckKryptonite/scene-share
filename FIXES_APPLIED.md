# SceneShare Internal Server Error Fixes

## Issue Summary
The assessment feedback highlighted that internal server errors (500) were being generated when:
1. A user reviewed a newly searched movie from TMDB not already in the database
2. A user attempted to leave a review again on the same movie

## Root Causes Identified
1. **Duplicate review constraint violation** — The Review model has `unique_together = ('movie', 'user')`, but `add_review()` was doing a plain `save()` without handling duplicates, causing an `IntegrityError` when a user tried to review the same movie twice.

2. **Template context variable mismatch** — The `movie_detail()` view passed `review_form` to the template, but `detail.html` was referencing `form`, causing form field access errors.

3. **Redirect assumes tmdb_id exists** — For non-TMDB movies without a `tmdb_id`, the redirect would fail or throw an error.

## Changes Made

### 1. **movies/views.py** (add_review function)
- **Before**: Used `review.save()` which violated the unique constraint on duplicate submissions
- **After**: Changed to `Review.objects.update_or_create()` to handle both new and existing reviews gracefully
- **Additional**: Added try/except block to catch any unforeseen database errors
- **Fallback**: If movie lacks `tmdb_id`, redirects to home instead of failing

### 2. **movies/templates/movies/detail.html** (review form)
- **Before**: Used `{{ form }}` and `form.rating`, `form.comment` — variable name mismatch
- **After**: Changed all references to `{{ review_form }}` to match the context variable passed from the view

## Result
✅ Users can now review newly searched TMDB movies without errors  
✅ Users can update their review by submitting the form again (update-or-create logic)  
✅ No more 500 errors on duplicate review attempts  
✅ Form displays and pre-fills correctly on the detail page  

## Testing Recommendation
1. Search for a movie not in your database
2. View its detail page
3. Submit a review — should succeed with a success message
4. Try to submit another review on the same movie — should update the existing review, not throw an error
5. Check that the updated review displays correctly on the page
