from rest_framework import serializers
from .models import Leave
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from employee.models import Employee
from django.utils import timezone

class SeeLeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = "__all__"


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        exclude = ["employee","statustype"]

    def validate(self, attrs):
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        today=timezone.localdate()
        if start_date and end_date and end_date < start_date:
            raise serializers.ValidationError({"error": "End date cannot be before start date."})
        if start_date and start_date < today:
            raise serializers.ValidationError({"error": "Start date is before today"})
        
        try:
            employee = self.context["request"].user.employee
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"error": "Employee does not exist"})

        if employee.is_active== Employee.Status.INACTIVE:
            raise serializers.ValidationError({"error":"You are Inactive"})
        existing=Leave.objects.filter(employee=employee,start_date=start_date,end_date=end_date,statustype=Leave.StatusType.PENDING).exists()

        if existing:
            raise serializers.ValidationError({"error": "A pending leave request for these dates already exists."})

        return attrs
    
class LeaveStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = ["statustype"]

    def validate_statustype(self, value):
        if value not in [
            Leave.StatusType.APPROVED,
            Leave.StatusType.REJECTED
        ]:
            raise serializers.ValidationError("Status can only be Approved or Rejected.")
        return value