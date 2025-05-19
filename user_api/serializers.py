from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model.

    Handles validation of user data during CSV processing.
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'age']

    def validate_name(self, value):
        """Validate that the name field is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Name cannot be empty")
        return value

    def validate_age(self, value):
        """Validate that age is an integer between 0 and 120."""
        if not isinstance(value, int) or value < 0 or value > 120:
            raise serializers.ValidationError(
                "Age must be an integer between 0 and 120"
            )
        return value
