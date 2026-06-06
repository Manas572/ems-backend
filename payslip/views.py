from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from employee.permissions import IsAdmin
from .models import Payslip
from .serializers import SeePaySlipSerializer,PaySlipSerializer
from rest_framework.throttling import UserRateThrottle
# Create your views here.
class ApiThrottle(UserRateThrottle):
    rate = "50/min"
#create payslip
class CreatePaySlip(CreateAPIView):
    throttle_classes=[ApiThrottle]
    permission_classes = [IsAdmin]
    queryset = Payslip.objects.all().order_by("-created_at")
    serializer_class = PaySlipSerializer
    
#get pending leave
class SeePaySlip(ListAPIView):
    throttle_classes=[ApiThrottle]
    permission_classes=[IsAdmin]
    queryset=Payslip.objects.all()
    serializer_class=SeePaySlipSerializer

class SeeYourPaySlip(ListAPIView):
    throttle_classes=[ApiThrottle]
    serializer_class = SeePaySlipSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        try:
            employee = self.request.user.employee
        except ObjectDoesNotExist:
            return Payslip.objects.none()
        queryset = Payslip.objects.filter(employee=employee).order_by("-created_at")
        return queryset
        
#1 payslip
class PaySlipDetail(RetrieveAPIView):
    throttle_classes=[ApiThrottle]
    serializer_class = SeePaySlipSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        if self.request.user.role == "ADMIN":
            return Payslip.objects.all()
        try:
            employee = self.request.user.employee
            return Payslip.objects.filter(employee=employee)
        except ObjectDoesNotExist:
            return Payslip.objects.none()