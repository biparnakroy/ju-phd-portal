from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage  # To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json

from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.renderers import JSONRenderer

from juphd_app.models import CustomUser, Admin, Prof, Student, Department, StudentResult
import uuid
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from juphd_app.EmailBackEnd import EmailBackEnd
import requests
# settings 
from django.conf import settings

# Student Profile View
class StudentProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        student = Student.objects.get(user=request.user)
        context = {
            'student': student,
        }
        return render(request, 'student/student_profile.html', context)

# Student Profile Edit View
class studentProfileEditView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        student = Student.objects.get(user=request.user)
        departments = Department.objects.all()
        context = {
            'student': student,
            'departments': departments,
        }
        return render(request, 'student/student_profile_edit.html', context)

# Student Profile Edit 
class StudentProfileEdit(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        student = Student.objects.get(user=request.user)
        student.user.first_name = request.POST.get('first_name')
        student.user.last_name = request.POST.get('last_name')
        student.user.email = request.POST.get('email')
        student.user.username = request.POST.get('username')
        

        # profile picture upload
        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            ext = profile_pic.name.split('.')[-1]
            fs = FileSystemStorage()
            filename =   filename = 'student/' + student.user.first_name+'__'+student.user.last_name + '__' + str(uuid.uuid4()) + '.' + ext
            filename = fs.save(filename, profile_pic)
            student.profile_pic = fs.url(filename)

        # password change
        if request.POST.get('password'):
            student.user.set_password(request.POST.get('password'))
            student.user.save()
            # re-authenticate user
            user = EmailBackEnd.authenticate(request, username=student.user.email, password=request.POST.get('password'))
            if user is not None:
                login(request, user)
            else :
                return redirect('login')

        student.user.save()
        student.save()
        messages.success(request, "Profile Updated Successfully!")
        return redirect('student_profile')


# Student Home Page
class Student_home(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.user_type == '3':
            student = Student.objects.get(user=request.user)
            student_result = StudentResult.objects.filter(student_result_student=student)
            context = {
                'student': student,
                'student_result': student_result,
            }

            return render(request, 'student/student_home.html', context)
        else:
            return redirect('login')

# Student Prof View
class StudentProfView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.user_type == '3':
            student = Student.objects.get(user=request.user)
            context = {
                'prof': student.prof_under,
            }
            return render(request, 'student/student_prof.html', context)
        else:
            return redirect('login')

# Student Result View
class StudentResultView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.user_type == '3':
            student = Student.objects.get(user=request.user)
            # does student have result
            if  StudentResult.objects.filter(student_result_student=student).exists():
                student_result = StudentResult.objects.get(student_result_student=student)
            else :
                student_result = None
            context = {
                'student': student,
                'student_result': student_result,
            }
            return render(request, 'student/student_result.html', context)
        else:
            return redirect('login')

# Student Change Title of thesis view 
class StudentChangeTitleView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.user_type == '3':
            student = Student.objects.get(user=request.user)
            context = {
                'student': student,
            }
            return render(request, 'student/student_change_title.html', context)
        else:
            return redirect('login')

    def post(self, request):
        if request.user.user_type == '3':
            student = Student.objects.get(user=request.user)
            student.changed_title_of_thesis = request.POST.get('changed_title_of_thesis')
            student.has_changed_title_of_thesis = True
            student.save()
            messages.success(request, "Title Updated Successfully!")
            return redirect('student_home')
        else:
            return redirect('login')

