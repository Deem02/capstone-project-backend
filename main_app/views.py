from django.shortcuts import render
from .models import Department, Employee
from .serializers import DepartmentSerializer, EmployeeSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
#Auth
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny, IsAdminUser

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

# retreve, update, delete a single department         
class DepartmentDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, department_id ):
        try:
            department = get_object_or_404(Department, id=department_id)
            serializer = DepartmentSerializer(department)
            data = serializer.data
            return Response(data)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def put(self, request, department_id):
        
        try:
            department = get_object_or_404(Department, id=department_id)
            serializer = DepartmentSerializer(department, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)           
              
        except Exception as err:
                return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    def delete(self, request, department_id):
        department = get_object_or_404(Department, id=department_id)
        department.delete()
        return Response({'message': f'Depatment {department_id} has been dealeted '}, status=status.HTTP_200_OK)
    # I dont use try - except here to get  404 Not Found 
    
class EmployeeRegister(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):     
        try:
            serializer = EmployeeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)           
        
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
   
   
    def get(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
       
class EmployeeDetail(APIView):
    permission_classes = [AllowAny] 
    def get(self, request, employee_id ):
        try:
            employee = get_object_or_404(Employee, id=employee_id)
            serializer = EmployeeSerializer(employee)
            data = serializer.data
            return Response(data)
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request, employee_id):
        
        try:
            employee = get_object_or_404(Employee, id=employee_id)
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)                       
        except Exception as err:
            return Response({'error': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
          
    def delete(self, request, employee_id):
        employee = get_object_or_404(Employee, id=employee_id)
        user = employee.user
        user.delete()
        return Response({'message': f'Employee {employee_id} and their user account has been deleted '}, status=status.HTTP_200_OK)
                  
                  
                  
  
        
            
            
    
        
        
        
