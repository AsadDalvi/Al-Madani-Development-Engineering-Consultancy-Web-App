from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Feedback, Inquiry, FloorPlan

# Registration Form for creating a user
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Automatically set role to 'client' for clients
        self.instance.role = CustomUser.CLIENT


# Feedback Form for submitting feedback with a rating
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['message', 'rating']  # Include both message and rating fields

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')
        return rating


# Inquiry Form for clients to submit inquiries
class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['subject', 'message']  # Includes subject and message fields


# Floor Plan Form for employees to upload floor plans
class FloorPlanForm(forms.ModelForm):
    class Meta:
        model = FloorPlan
        fields = ['title', 'file']
