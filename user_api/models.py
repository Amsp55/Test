from django.db import models


class User(models.Model):
    """Model for storing user information from CSV uploads.

    This model represents a user with basic information including name,
    email, and age. The email field is unique to prevent duplicates.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return a string representation of the user."""
        return self.name
