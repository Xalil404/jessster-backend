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

        # Check if profile_picture is in the request data, if not, retain the current profile_picture
        if 'profile_picture' not in data:
            data['profile_picture'] = instance.profile_picture

        # Serialize the data
        serializer = self.get_serializer(instance, data=data, partial=partial)

        # Validate and update
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)