# views.py 
from django.shortcuts import render
import json
from google.oauth2 import id_token
from google.auth.transport.requests import Request
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
import logging
from google.auth.transport import requests
from django.conf import settings

logger = logging.getLogger(__name__)

# View for web pop-up ux
@csrf_exempt
def google_auth(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        token = body.get('token')

        try:
            # Verify the token with Google
            idinfo = id_token.verify_oauth2_token(
                token,
                Request(),  # Use the correct Request object
                "387788518673-vqgk8blm21alfiungj28pji8tte51jd4.apps.googleusercontent.com"
            )
            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')

            # Check if user exists; if not, create a new one
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

            # Create or get a token for the user
            token, _ = Token.objects.get_or_create(user=user)

            return JsonResponse({'token': token.key}, status=200)

        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


# Mobile app authentication
@csrf_exempt
def google_auth_mobile(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        token = body.get('token')

        try:
            # Verify the token with Google for the mobile client ID 
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), "484109282478-g7ssevh8nrvng492cnn9vie63a9rfia1.apps.googleusercontent.com")
            email = idinfo['email']
            first_name = idinfo.get('given_name', '')
            last_name = idinfo.get('family_name', '')

            # Check if user exists; if not, create a new one
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email.split('@')[0],
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

            # Create or get a token for the user
            token, _ = Token.objects.get_or_create(user=user)

            return JsonResponse({'token': token.key}, status=200)

        except ValueError:
            return JsonResponse({'error': 'Invalid token'}, status=400)

    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
