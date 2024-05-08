from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, logout
from django.shortcuts import redirect
from .models import Transaction
from .serializers import TransactionSerializer
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'myapp/index.html')

class TransactionListCreate(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class TransactionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# Remove the logout_view function

class SomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        # Your logic for GET request
        return Response({'message': 'GET request processed'})

    def post(self, request, format=None):
        # Your logic for POST request
        return Response({'message': 'POST request processed'})

    def put(self, request, format=None):
        # Your logic for PUT request
        return Response({'message': 'PUT request processed'})

    def patch(self, request, format=None):
        # Your logic for PATCH request
        return Response({'message': 'PATCH request processed'})

    def delete(self, request, format=None):
        # Your logic for DELETE request
        return Response({'message': 'DELETE request processed'})
