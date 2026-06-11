from django.shortcuts import render
from rest_framework.generics import DestroyAPIView,UpdateAPIView,ListAPIView,CreateAPIView,RetrieveAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from .models import Employee,User
from .serializers import EmployeeSerializer,EmployeeCreateSerializer
from .permissions import IsAdmin
from rest_framework.throttling import UserRateThrottle


class ApiThrottle(UserRateThrottle):
    rate = "60/min"
# Create your views here.
# create
class EmpCreate(CreateAPIView):
    throttle_classes=[ApiThrottle]
    serializer_class=EmployeeCreateSerializer
    permission_classes=[IsAdmin]
    queryset=User.objects.all()
    

#get
class EmpGetList(ListAPIView):
    throttle_classes=[ApiThrottle]
    serializer_class = EmployeeSerializer
    permission_classes=[IsAdmin]
    def get_queryset(self):
        queryset = Employee.objects.filter(is_deleted=False)
        department = self.request.query_params.get("department")
        if department:
            queryset = queryset.filter(department=department)
        return queryset


#get list
class EmployeeSearchView(ListAPIView):
    throttle_classes=[ApiThrottle]
    queryset = Employee.objects.filter(is_deleted=False).order_by("-created_at")
    permission_classes=[IsAdmin]
    serializer_class = EmployeeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["firstname", "lastname", "department"]

class EmployeeDetail(RetrieveAPIView):
    throttle_classes=[ApiThrottle]
    queryset = Employee.objects.filter(is_deleted=False)
    permission_classes=[IsAuthenticated]
    serializer_class = EmployeeSerializer

#update
class EmpUpdate(UpdateAPIView):
    throttle_classes=[ApiThrottle]
    queryset=Employee.objects.filter(is_deleted=False)
    permission_classes=[IsAdmin]
    serializer_class=EmployeeSerializer


#delete
class EmpDelete(DestroyAPIView):
    throttle_classes=[ApiThrottle]
    serializer_class = EmployeeSerializer
    permission_classes=[IsAdmin]
    queryset = Employee.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

