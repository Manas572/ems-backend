from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from employee.permissions import IsAdmin
from .models import Leave
from .serializers import SeeLeaveSerializer,LeaveSerializer,LeaveStatusSerializer
from rest_framework.throttling import UserRateThrottle
# Create your views here.
class ApiThrottle(UserRateThrottle):
    rate = "50/min"
#create leave
class CreateLeave(CreateAPIView):
    throttle_classes=[ApiThrottle]
    permission_classes = [IsAuthenticated]
    queryset = Leave.objects.all()
    serializer_class = LeaveSerializer
    def perform_create(self, serializer):
        serializer.save(
            employee=self.request.user.employee
        )

        
#get pending leave
class SeeLeaves(ListAPIView):
    throttle_classes=[ApiThrottle]
    permission_classes=[IsAdmin]
    queryset=Leave.objects.filter(statustype=Leave.StatusType.PENDING).order_by("-created_at")
    serializer_class=SeeLeaveSerializer

#see yourleave
class SeeYourLeave(ListAPIView):
    throttle_classes=[ApiThrottle]
    serializer_class = SeeLeaveSerializer
    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        try:
            employee = self.request.user.employee
        except ObjectDoesNotExist:
            return Leave.objects.none()
        queryset = Leave.objects.filter(employee=employee).order_by("-created_at")
        return queryset
        

#update leave
class UpdateLeave(UpdateAPIView):
    throttle_classes=[ApiThrottle]
    permission_classes = [IsAdmin]
    serializer_class = LeaveStatusSerializer
    def get_queryset(self):
        return Leave.objects.filter(statustype=Leave.StatusType.PENDING)
