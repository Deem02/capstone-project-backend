from rest_framework import serializers
from .models import Department, Employee
from django.contrib.auth import get_user_model
from django.db import  transaction

User = get_user_model()


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        

        
class UserSerializer(serializers.ModelSerializer):
    #read only to show user detail in GET
    class Meta:
        model = User
        fields =('id','first_name', 'last_name', 'email','username')
        
        
class EmployeeSerializer(serializers.ModelSerializer):

    # Fileds for creating new user write_only
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    
    #used nested serializer to show user detail
    user = UserSerializer(read_only=True)
    # to show name of department
    department  = serializers.StringRelatedField(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department',write_only=True,allow_null=True )
    
    employee_id= serializers.IntegerField(source='id',read_only=True)    

    class Meta:
        model = Employee
        fields = ('employee_id','user','department', 'role',
                  'department_id', 
                  'username','email','first_name','last_name','password')
   
 # create new user then the employee 
    @transaction.atomic  # to ensure both objects are created or neither
    def create(self, validated_data):
        user_data=  {
        'username': validated_data.pop('username'),
        'email': validated_data.pop('email'),
        'first_name' : validated_data.pop('first_name'),
        'last_name' : validated_data.pop('last_name'),
      }
        password = validated_data.pop('password')
        
        user = User.objects.create_user(**user_data, password=password)
        employee = Employee.objects.create(user=user,**validated_data )
        return employee    
    
    
