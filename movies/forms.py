from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Form for submitting a review, including a star rating and a comment.
    Uses radio buttons for rating selection and a textarea for the comment.
    """
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(
                choices=[(i, '⭐' * i) for i in range(1, 6)]
            ),
            'comment': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 3,
                    'placeholder': 'Write your review...'
                }
            ),
        }