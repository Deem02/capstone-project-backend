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

    # Fileds for creating/updating new user write_only
    username = serializers.CharField(write_only=True, required=False)
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    
    #Read only fileds for GET
    #used nested serializer to show user detail
    user = UserSerializer(read_only=True)
    # to show name of department
    department  = serializers.StringRelatedField(read_only=True)
    employee_id= serializers.IntegerField(source='id',read_only=True)  
    # Write only field for assocations  
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department',write_only=True,allow_null=True )

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
    
    @transaction.atomic  # to ensure both objects are created or neither
    def update(self,instance, validated_data):
        #instance: existing Employee objet
        user =  instance.user # User object that is linked to Employee
        
        #pop and update User data if provided
        user.username =validated_data.pop('username',user.username)
        user.password = validated_data.pop('password',user.password)
        user.email = validated_data.pop('email',user.email)
        user.first_name = validated_data.pop('first_name',user.first_name)
        user.last_name = validated_data.pop('last_name',user.last_name)
             
        user.save()
        #update Employee data
        instance.role=validated_data.get('role', instance.role)
        instance.department=validated_data.get('department', instance.department)
        instance.save()
        return instance
        
    
    
