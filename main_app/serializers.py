from rest_framework import serializers
from .models import Department, Employee
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import  transaction

User = get_user_model()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
                
class UserSerializer(serializers.ModelSerializer):                    #allow empty string on updates
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)  
    #read only to show user detail in GET
    class Meta:
        model = User
        fields =('id','first_name', 'last_name', 'email','username','password')
        extra_kwargs = {
               'username': {
                'validators':[UnicodeUsernameValidator()],
        }
        }   
# create/update            
class EmployeeSerializer(serializers.ModelSerializer):
    # nested serializer for both  reading/writing
    user = UserSerializer()
    
    #Read only fileds for clear represention in GET request
    # to show name of department
    department  = serializers.StringRelatedField(read_only=True)
    employee_id= serializers.IntegerField(source='id',read_only=True) 

    #field for assocations  
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department',allow_null=True,required=False, write_only=True )
   
    class Meta:
        model = Employee
        fields = ('employee_id','user','department', 'role',
                  'department_id', 
     )
 
    def validate(self,data):
        #cutome validate to handel usename and email in creating/updating
        user_data = data.get('user')
        if not user_data or "username" not in user_data:
            return data
        
        
        if 'username' in user_data:
            username = user_data['username']
            if self.instance:
            #for update 
                if User.objects.filter(username=username).exclude(pk=self.instance.user.pk).exists():
                    raise serializers.ValidationError({'user':{ "This username is already taken."}})  
            else: 
                #create
                if User.objects.filter(username=username).exists():
                    raise serializers.ValidationError({'user':{ "A user with that username is already exists."}})
                
        if 'email' in user_data:            
            email = user_data['email']
            if self.instance:
                #for update 
                if User.objects.filter(email=email).exclude(pk=self.instance.user.pk).exists():
                    raise serializers.ValidationError({'user':{ "A user with this email is already taken."}})  
            else: 
                #create
                if User.objects.filter(email=email).exists():
                    raise serializers.ValidationError({'user':{ "A user with this email is already exists."}})  
            
        return data
            
 # create new user then the employee 
    @transaction.atomic  # to ensure both objects are created or neither
    def create(self, validated_data):
        user_data = validated_data.pop('user') 
        password = user_data.pop('password')
        
        user = User.objects.create_user(**user_data, password=password)
        employee = Employee.objects.create(user=user,**validated_data )
        return employee 
    
    #Handel the update of Employee and its User
    @transaction.atomic  # to ensure both objects are created or neither
    def update(self,instance, validated_data):
        #instance: existing Employee objet
        # Get user_data, defult {} if user isn't provided
        user_data = validated_data.pop('user',{})
        user = instance.user # User object that is linked to Employee
        #pop and update password if provided
        password = user_data.pop('password',None)
        if password:
            user.set_password(password) 
        #Update all other user fileds sent in user_data
        #if user_data is {} skipp the loop   
        for key, value in user_data.items():
            setattr(user, key, value)    
        user.save()
        #update Employee data
        # instance.role=validated_data.get('role', instance.role)
        # instance.department=validated_data.get('department', instance.department)
        # instance.save()
        super().update(instance=instance, validated_data=validated_data)
        return instance
    
class EmployeeListSerializer(serializers.ModelSerializer):
        # read only for displying in EmplyeeList view
        username = serializers.CharField(source='user.username')
        department  = serializers.StringRelatedField()
        role = serializers.CharField(source='get_role_display') 
        first_name=serializers.CharField(source='user.first_name')
        last_name=serializers.CharField(source='user.last_name')
        email=serializers.CharField(source='user.email')
        class Meta:
            model = Employee
            fields = ('id','username','first_name', 'last_name', 'email', 'department', 'role')
            
        
    
    # Refrence:
    #https://medium.com/django-rest-framework/dealing-with-unique-constraints-in-nested-serializers-dade33b831d9
        
    
    
