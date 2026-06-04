from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import CreateAPIView,ListAPIView,RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from employee.permissions import IsAdmin
from .models import Payslip
from .serializers import SeePaySlipSerializer,PaySlipSerializer

# Create your views here.
#create payslip
class CreatePaySlip(CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Payslip.objects.all()
    serializer_class = PaySlipSerializer
    
#get pending leave
class SeePaySlip(ListAPIView):
    permission_classes=[IsAdmin]
    queryset=Payslip.objects.all()
    serializer_class=SeePaySlipSerializer

class SeeYourPaySlip(ListAPIView):
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