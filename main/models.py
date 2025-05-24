from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User Model for Clients & Employees
class CustomUser(AbstractUser):  
    CLIENT = 'Client'
    EMPLOYEE = 'Employee'

    ROLE_CHOICES = [
        (CLIENT, 'Client'),
        (EMPLOYEE, 'Employee'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=CLIENT)

    def __str__(self):
        return f"{self.username} ({self.role})"


# Model for Feedback
class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Link feedback to CustomUser
    message = models.TextField()  # Message field for feedback
    rating = models.PositiveIntegerField(default=5, choices=[(i, i) for i in range(1, 6)])  # Rating field, 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically stores the time of feedback made

    def __str__(self):
        return f"Feedback from {self.user.username} - Rating: {self.rating}"


# Model for Inquiries
class Inquiry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Client name who submitted inquiry
    subject = models.CharField(max_length=255)  # Inquiry subject
    message = models.TextField()  # Inquiry message
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically stores the time of inquiry made

    def __str__(self):
        return f"Inquiry from {self.user.username}: {self.subject}"


# Model for Floor Plans (Employee Only)
class FloorPlan(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='floor_plans/')  # Uploads PDFs
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# Model for Gallery
class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')  # Uploads images to gallery folder thru Django admin panel

    def __str__(self):
        return f"Gallery Image {self.id}"
