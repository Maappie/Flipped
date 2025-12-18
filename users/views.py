from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.oauth2 import id_token
from google.auth.transport import requests
from .serializers import GoogleLoginSerializer
from rest_framework.permissions import AllowAny

# 1. The API Logic (Handles the token from Google)
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data['access_token']

        try:
            # Verify the token with Google
            id_info = id_token.verify_oauth2_token(token, requests.Request())

            # Extract User Info
            email = id_info['email']
            first_name = id_info.get('given_name', '')
            last_name = id_info.get('family_name', '')

            # Find or Create the User
            user, created = User.objects.get_or_create(
                username=email,
                defaults={
                    'email': email,
                    'first_name': first_name,
                    'last_name': last_name,
                }
            )

            # Log the User In
            login(request, user)

            return Response({
                'message': 'Login Successful',
                'user': user.email
            }, status=status.HTTP_200_OK)

        except ValueError:
            return Response({'error': 'Invalid Google Token'}, status=status.HTTP_400_BAD_REQUEST)

# 2. The View Logic (Shows the HTML page)
def login_page(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('profile')
        elif user is None:
            return render(request, 'users/login.html', {'error': 'Account not Found'})
        else:
            return render(request, 'users/login.html', {'error' : 'Invalid Email or Password'})
        
            
    return render(request, 'users/login.html')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')

def logout_view(request):
    logout(request)
    return redirect('/')