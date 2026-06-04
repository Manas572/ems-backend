from django.db import models
from employee.models import Employee
# Create your models here.
class Leave(models.Model):
    class StatusType(models.TextChoices):
        PENDING="PENDING","Pending",
        APPROVED="APPROVED","Approved",
        REJECTED="REJECTED","Rejected"

    class LeaveType(models.TextChoices):
        SICK="SICK","Sick",
        CASUAL="CASUAL","Casual",
        ANNUAL="ANNUAL","Annual"
    
    employee=models.ForeignKey(
        "employee.Employee",
        on_delete=models.CASCADE,
        related_name="leave_application"
    )
    start_date = models.DateField()
    end_date = models.DateField()
    reason=models.TextField(max_length=100)
    statustype=models.CharField(max_length=15,choices=StatusType.choices,default=StatusType.PENDING)
    leavetype=models.CharField(max_length=15,choices=LeaveType.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

