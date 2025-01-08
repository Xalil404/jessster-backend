from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .models import Subscriber
from .serializers import SubscriberSerializer

# View to subscribe to newsletter
class SubscribeView(generics.CreateAPIView):
    serializer_class = SubscriberSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        email = request.data.get('email')

        # Check if the email already exists in the database
        if Subscriber.objects.filter(email=email).exists():
            return Response({'message': 'You are already subscribed!'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)
