from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)
    
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        EMPLOYEE = "EMPLOYEE", "Employee"  
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.EMPLOYEE
    )
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()


class Employee(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        INACTIVE = "INACTIVE", "Inactive"
        
    class Department(models.TextChoices):
        ENGINEERING = "Engineering", "Engineering"
        HUMAN_RESOURCES = "Human Resources", "Human Resources"
        MARKETING = "Marketing", "Marketing"
        SALES = "Sales", "Sales"
        FINANCE = "Finance", "Finance"
        OPERATIONS = "Operations", "Operations"
        IT_SUPPORT = "IT Support", "IT Support"
        CUSTOMER_SUCCESS = "Customer Success", "Customer Success"
        PRODUCT_MANAGEMENT = "Product Management", "Product Management"
        DESIGN = "Design", "Design"

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="employee"
    )

    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    position = models.CharField(max_length=50)
    basicsalary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    is_deleted = models.BooleanField(default=False)
    joining_date = models.DateField()
    department = models.CharField(max_length=30, choices=Department.choices)
    bio = models.TextField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    @property
    def email(self):
        return self.user.email