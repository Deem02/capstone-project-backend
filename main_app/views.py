from django.shortcuts import render
from .models import Department
from .serializers import DepartmentSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
#Auth
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth import get_user_model

# Create your views here.

class DepartmentList(APIView):
    
    # Auth
    # Note: even if i dont add it here it will still be protected by a golabal settins in REST_FRAMEWORK
    permission_classes = [IsAuthenticated]
      
    def get(self, request):
        queryset = Department.objects.all()
        serializer = DepartmentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        
        try:
            serializer = DepartmentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)           
        
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        
