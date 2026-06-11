"""
URL configuration for emsbackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
#import inngest.django
from employee.views import EmpGetList, EmpCreate,EmpUpdate,EmpDelete,EmployeeSearchView
from attendance.views import CheckIn,CheckOut,GetAllAttendance,GetYourAttendance,Hi
from leave.views import CreateLeave,UpdateLeave,SeeLeaves,SeeYourLeave
from payslip.views import SeeYourPaySlip,SeePaySlip,CreatePaySlip,PaySlipDetail
#from attendance.inngest_functions import auto_checkout_cron
#from .inngest_client import inngest_client

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', Hi.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('allemployees/', EmpGetList.as_view(), name='All_employees'),
    path('list/', EmployeeSearchView.as_view(), name='employee-list'),
    path('employee/create/', EmpCreate.as_view(), name='Create_Employee'),
    path('employee/update/<int:pk>/', EmpUpdate.as_view(), name='Update_Employee'),
    path('employee/delete/<int:pk>/', EmpDelete.as_view(), name='Delete_Employee'),
    path('attendance/checkin/', CheckIn.as_view(), name='checkin_Employee'),
    path('attendance/checkout/', CheckOut.as_view(), name='checkout_Employee'),
    path('attendance/allAttendance/', GetAllAttendance.as_view(), name='All_Attendance'),
    path('attendance/EmpAttendance/', GetYourAttendance.as_view(), name='Employee_Attendance'),
    path('leave/CreateLeave/', CreateLeave.as_view(), name='Create_Leave'),
    path('leave/SeeLeaves/', SeeLeaves.as_view(), name='See_Leave '),
    path('leave/SeeYourLeaves/', SeeYourLeave.as_view(), name='See_Your_Leave '),
    path('leave/update/<int:pk>/', UpdateLeave.as_view(), name='Update_Leave '),
    path('payslip/Createpayslip/', CreatePaySlip.as_view(), name='Create_Payslip'),
    path('payslip/Seepayslip/', SeePaySlip.as_view(), name='See_Payslip '),
    path('payslip/SeeYourPayslip/', SeeYourPaySlip.as_view(), name='See_Your_Payslip '),
    path('payslip/detail/<int:pk>/', PaySlipDetail.as_view(), name='Payslip_Detail '),
   # inngest.django.serve(inngest_client, [auto_checkout_cron]),
]
