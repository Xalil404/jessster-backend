from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    # Optional: Include username or other user-specific details
    username = serializers.CharField(source='user.username', read_only=True)  # If you want to include username
    email = serializers.EmailField(source='user.email', read_only=True) 

    class Meta:
        model = Profile
        fields = ['id', 'bio', 'profile_picture', 'username', 'email']  # Add more fields if needed
    
    def update(self, instance, validated_data):
    # Only update fields present in validated_data
        for attr, value in validated_data.items():
            if value is None and attr == 'profile_picture':
                setattr(instance, attr, None)  # Set the profile picture to None
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


