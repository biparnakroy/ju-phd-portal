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

from juphd_app.models import CustomUser,Department, Prof, Student, StudentResult
import uuid
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from juphd_app.EmailBackEnd import EmailBackEnd
import requests
# settings 
from django.conf import settings


from .helper import render_to_pdf
from django.template.loader import get_template



# Prof Profile View
class ProfProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        prof = Prof.objects.get(user=request.user)
        context = {
            'prof': prof,
        }
        return render(request, 'prof/prof_profile.html', context)



# Prof Profile Edit View
class ProfProfileEditView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        prof = Prof.objects.get(user=request.user)
        departments = Department.objects.all()
        context = {
            'prof': prof,
            'departments': departments,
        }
        return render(request, 'prof/prof_profile_edit.html', context)

# Prof Profile Edit 
class ProfProfileEdit(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        prof = Prof.objects.get(user=request.user)
        prof.user.first_name = request.POST.get('first_name')
        prof.user.last_name = request.POST.get('last_name')
        prof.user.email = request.POST.get('email')
        prof.user.username = request.POST.get('username')
        #prof.prof_faculty = request.POST.get('prof_faculty')
        #prof.prof_dept = Department.objects.get(dept_uuid=request.POST.get('department'))

        # profile picture upload
        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            ext = profile_pic.name.split('.')[-1]
            fs = FileSystemStorage()
            filename =   filename = 'prof/' + prof.user.first_name+'__'+prof.user.last_name + '__' + str(uuid.uuid4()) + '.' + ext
            filename = fs.save(filename, profile_pic)
            prof.profile_pic = fs.url(filename)

        # password change
        if request.POST.get('password'):
            prof.user.set_password(request.POST.get('password'))
            prof.user.save()
            # re-authenticate user
            user = EmailBackEnd.authenticate(request, username=prof.user.email, password=request.POST.get('password'))
            if user is not None:
                login(request, user)
            else :
                return redirect('login')

        prof.user.save()
        prof.save()
        messages.success(request, "Profile Updated Successfully!")
        return redirect('prof_profile')


# Prof Home dashboard
class Prof_home(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '2':
            # calculate number of students under the prof
            student_count = Student.objects.filter(prof_under=Prof.objects.get(prof_uuid=request.user.prof.prof_uuid)).count()
            context = {
                'student_count': student_count,
            }

            return render(request, 'prof/prof_home.html', context)
        else:
            return redirect('login')


# Prof Student List View
class ProfStudentListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '2':
            students = Student.objects.filter(prof_under=Prof.objects.get(prof_uuid=request.user.prof.prof_uuid))
            context = {
                'students': students,
            }
            return render(request, 'prof/prof_student_list.html', context)
        else:
            return redirect('login')

# Prof Student View
class ProfStudentView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, student_uuid):
        if request.user.user_type == '2':
            student = Student.objects.get(student_uuid=student_uuid)
            context = {
                'student': student,
            }
            return render(request, 'prof/prof_student_view.html', context)
        else:
            return redirect('login')


# download student data into pdf
class Download_student_data(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, student_uuid):
        if request.user.user_type == '2':
            #student_uuid = request.GET.get('student_uuid')
            student = Student.objects.get(student_uuid=student_uuid)
            student_image = student.profile_pic.url
            ju_logo = 'static/images/logo.png'
            # deleting the first letter of the student_image
            student_image = student_image[7:]
            context = {
                'student': student,
                'student_image': student_image,
                'ju_logo': ju_logo,
            }

            #template = get_template('pdf/student_data.html')
            #html = template.render(context)
            pdf = render_to_pdf('pdf/student_data.html', context)
            if pdf:
                response = HttpResponse(pdf, content_type='application/pdf')
                filename = "%s.pdf" %(str(student.user.first_name)+'__'+str(student.user.last_name))
                print(filename)
                content = "inline; filename='%s'" %(filename)
                download = True
                if download:
                    content = "attachment; filename='%s'" %(filename)
                response['Content-Disposition'] = content
                # auto download the file
                # response['Content-Length'] = len(response.content)
                # response['Content-Type'] = 'application/octet-stream'
                # response['Content-Transfer-Encoding'] = 'binary'
                # response['Content-Disposition'] = 'attachment; filename="%s"' %(filename)

                return response

            # pdf = render_to_pdf('pdf/student_data.html', context)
            # return HttpResponse(pdf, content_type='application/pdf')
            return HttpResponse("Not found")
        else:
            return redirect('login')

# Prof Student Result List View
class ProfStudentResultListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '2':
            student_results = StudentResult.objects.filter(student_result_student__prof_under=Prof.objects.get(prof_uuid=request.user.prof.prof_uuid))

            context = {
                'student_results': student_results,
            }
            return render(request, 'prof/prof_student_result_list.html', context)
        else:
            return redirect('login')

# Prof Student Result View
class ProfStudentResultView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, student_uuid):
        if request.user.user_type == '2':
            student_result = StudentResult.objects.get(student_result_student__student_uuid=student_uuid)
            context = {
                'student_result': student_result,
            }
            return render(request, 'prof/prof_student_result_view.html', context)
        else:
            return redirect('login')