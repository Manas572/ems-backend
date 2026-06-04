from django.shortcuts import render
from rest_framework.generics import DestroyAPIView,UpdateAPIView,ListAPIView,CreateAPIView,RetrieveAPIView
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from .models import Employee,User
from .serializers import EmployeeSerializer,EmployeeCreateSerializer
from .permissions import IsAdmin
# Create your views here.
# create
class EmpCreate(CreateAPIView):
    serializer_class=EmployeeCreateSerializer
    permission_classes=[IsAdmin]
    queryset=User.objects.all()
    

#get
class EmpGetList(ListAPIView):
    serializer_class = EmployeeSerializer
    permission_classes=[IsAdmin]
    def get_queryset(self):
        queryset = Employee.objects.filter(is_deleted=False)
        department = self.request.query_params.get("department")
        if department:
            queryset = queryset.filter(department=department)
        return queryset


#get 1
class EmployeeSearchView(ListAPIView):
    queryset = Employee.objects.filter(is_deleted=False)
    permission_classes=[IsAuthenticated]
    serializer_class = EmployeeSerializer
    filter_backends = [SearchFilter]
    search_fields = ["firstname", "lastname", "email"]

class EmployeeDetail(RetrieveAPIView):
    queryset = Employee.objects.filter(is_deleted=False)
    permission_classes=[IsAuthenticated]
    serializer_class = EmployeeSerializer

#update
class EmpUpdate(UpdateAPIView):
    queryset=Employee.objects.filter(is_deleted=False)
    permission_classes=[IsAdmin]
    serializer_class=EmployeeSerializer


#delete
class EmpDelete(DestroyAPIView):
    serializer_class = EmployeeSerializer
    permission_classes=[IsAdmin]
    queryset = Employee.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
