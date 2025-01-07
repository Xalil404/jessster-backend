from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated

# Retrieve or update the logged-in user's profile
class ProfileDetailUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # This ensures the profile returned is the one related to the logged-in user
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
    # Enable partial updates (PATCH)
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

    # Make the request data mutable
        data = request.data.copy()

    # Handle case for removing profile picture (set to null)
        if 'profile_picture' in data and data['profile_picture'] == 'null':
            data['profile_picture'] = None  # Set to None to remove the profile picture

    # Serialize the data
        serializer = self.get_serializer(instance, data=data, partial=partial)

    # Validate and update
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
