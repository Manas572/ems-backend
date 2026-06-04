from rest_framework import serializers
from .models import Payslip
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from employee.models import Employee
from django.utils import timezone

class SeePaySlipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip
        fields = "__all__"


class PaySlipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip
        fields = "__all__"
        read_only_fields = ["net_salary"]

    def validate(self, attrs):
        employee = attrs.get("employee")
        month = attrs.get("month")
        year = attrs.get("year")
        current_year = timezone.now().year
        if month > 12:
            raise serializers.ValidationError({"error": "Month cannot be greater than 12"})
        if month < 1:
            raise serializers.ValidationError({"error": "Month cannot be less than 1"})
        if year < 2026 or year > current_year + 1:
            raise serializers.ValidationError({"error":"Invalid Year"})

        if Payslip.objects.filter(
            employee=employee,
            month=month,
            year=year
        ).exists():
            raise serializers.ValidationError({"error": "Payslip for this employee already exists for this month and year"})

        return attrs
