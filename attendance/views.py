from datetime import time
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle
from .models import Attendance
from employee.models import Employee
from rest_framework.generics import RetrieveAPIView,ListAPIView
from .serializers import AttendanceSerializer
from employee.permissions import IsAdmin

class ApiThrottle(UserRateThrottle):
    rate = "50/min"

class Hi(APIView):
    throttle_classes=[ApiThrottle]
    def get(self,request):
        return Response("hello")

class CheckIn(APIView):
    throttle_classes=[ApiThrottle]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            employee = request.user.employee
        except ObjectDoesNotExist:
            return Response({"error":"Employee Does Not Exist"} , status=status.HTTP_404_NOT_FOUND)
        
        today = timezone.localdate()
        if employee.is_active==Employee.Status.INACTIVE:
            return Response({"error":"Your account is inactive you cannot check in"},status=status.HTTP_403_FORBIDDEN)
        existing = Attendance.objects.filter(
            employee=employee,
            date=today
        ).first()

        if existing:
            return Response(
                {"error": "Already checked in today"},
                status=status.HTTP_400_BAD_REQUEST
            )

        current_time = timezone.localtime()
        office_time = time(9, 15)

        if current_time.time() > office_time:
            attendance_status = Attendance.Status.LATE
        else:
            attendance_status = Attendance.Status.PRESENT

        Attendance.objects.create(
            employee=employee,
            date=today,
            check_in=current_time,
            status=attendance_status
        )

        return Response(
            {"message": "Checked in successfully"},
            status=status.HTTP_201_CREATED
        )


class CheckOut(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes=[ApiThrottle]
    def post(self, request):
        try:
            employee = request.user.employee
        except ObjectDoesNotExist:
            return Response({"error":"Employee Does Not Exist"} , status=status.HTTP_404_NOT_FOUND)
        today = timezone.localdate()

        existing = Attendance.objects.filter(
            employee=employee,
            date=today
        ).first()

        if not existing:
            return Response(
                {"error": "You have not checked in today"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if existing.check_out:
            return Response(
                {"error": "You have checked out already"},
                status=status.HTTP_400_BAD_REQUEST
            )

        existing.check_out = timezone.localtime()

        hours = (
            existing.check_out - existing.check_in
        ).total_seconds() / 3600

        existing.working_hours = round(hours, 2)

        if hours >= 8:
            existing.day_type = Attendance.DayType.FULL_DAY
        elif hours >= 6:
            existing.day_type = Attendance.DayType.THREE_QUARTER_DAY
        elif hours >= 4:
            existing.day_type = Attendance.DayType.HALF_DAY
        else:
            existing.day_type = Attendance.DayType.SHORT_DAY

        existing.save()

        return Response(
            {"message": "Checked Out Successfully"},
            status=status.HTTP_200_OK
        )
    
class GetYourAttendance(ListAPIView):
    throttle_classes=[ApiThrottle]
    permission_classes=[IsAuthenticated]
    serializer_class=AttendanceSerializer
    def get_queryset(self):
        try:
            employee = self.request.user.employee
        except ObjectDoesNotExist:
            return Attendance.objects.none()
        queryset = Attendance.objects.filter(employee=employee).order_by("-created_at")
        return queryset

class GetAllAttendance(ListAPIView):
    throttle_classes=[ApiThrottle]
    permission_classes=[IsAdmin]
    queryset=Attendance.objects.all().order_by("-created_at")
    serializer_class=AttendanceSerializer


