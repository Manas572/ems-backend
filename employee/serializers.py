from rest_framework import serializers
from django.db import transaction
from .models import Employee,User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.utils import timezone

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        requested_portal = self.context['request'].data.get('portal_role')
        
        if requested_portal and getattr(self.user, 'role', None) != requested_portal:
            raise serializers.ValidationError(
                {"detail": f"Access denied. You do not have permission to access the {requested_portal} portal."}
            )

        if hasattr(self.user, 'employee'):
            employee = self.user.employee
            if employee.is_deleted or employee.is_active == "INACTIVE":
                raise serializers.ValidationError(
                    {"detail": "Your account has been deactivated. Please contact HR."}
                )

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        
        if hasattr(user, "employee"):
            token["firstname"] = user.employee.firstname
            token["department"] = user.employee.department

        return token
    

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = "__all__"

class EmployeeCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=User.Role.choices, write_only=True)
    firstname = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    phone = serializers.CharField(max_length=10)
    position = serializers.CharField(max_length=50)
    basicsalary = serializers.DecimalField(max_digits=10,decimal_places=2)
    allowances = serializers.DecimalField(max_digits=10,decimal_places=2,required=False,default=0)
    deductions = serializers.DecimalField(max_digits=10,decimal_places=2,required=False,default=0)
    department = serializers.ChoiceField(choices=Employee.Department.choices)
    joining_date = serializers.DateField()
    bio = serializers.CharField(max_length=150,required=False,allow_blank=True)

    @transaction.atomic
    def create(self, validated_data):
        password = validated_data.pop("password")
        role = validated_data.pop("role")
        email = validated_data.pop("email")
        
        user = User(
            email=email,
            role=role
        )
        user.set_password(password)
        user.save()
        employee = Employee.objects.create(user=user,**validated_data)

        return employee
    
    def validate(self, attrs):
        basicsalary=attrs.get("basicsalary")
        allowances=attrs.get("allowances")
        deductions=attrs.get("deductions")
        joining_date=attrs.get("joining_date")

        if basicsalary < 0:
            raise serializers.ValidationError({"error": "Basic salary cannot be negative"} )
        
        if allowances < 0:
            raise serializers.ValidationError({"error": "allowances cannot be negative"} )
        
        if deductions < 0:
            raise serializers.ValidationError({"error": "deductions cannot be negative"} )
        
        if basicsalary + allowances < deductions:
            raise serializers.ValidationError({"error": "Deductions cannot exceed total earnings"})
        
        today = timezone.localdate()

        if joining_date> today:
            raise serializers.ValidationError({"error":"Joining date cannot be before today"})
        
        return attrs
        
