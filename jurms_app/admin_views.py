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

from jurms_app.models import CustomUser, Admin, Prof, Student, Staff, Department, Course, StudentResult
import uuid



# Admin Home Dashboard
class Admin_home(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '1':
            # calculate number of students
            student_count = Student.objects.all().count()
            # calculate number of staff
            staff_count = Staff.objects.all().count()
            # calculate number of profs
            prof_count = Prof.objects.all().count()
            # calculate number of Departments
            dept_count = Department.objects.all().count()
            # calculate number of Courses
            course_count = Course.objects.all().count()

            # calculate Number of Students in each Department
            dept_student_count = {}
            for dept in Department.objects.all():
                dept_student_count[dept.dept_name] = Student.objects.filter(
                    student_department=dept).count()

            # calculate Number of Students in each Course
            course_student_count = {}
            for course in Course.objects.all():
                course_student_count[course.course_name] = Student.objects.filter(
                    student_course_list__icontains=course.course_name).count()

            # calculate Number of Courses in each Department
            dept_course_count = {}
            for dept in Department.objects.all():
                dept_course_count[dept.dept_name] = Course.objects.filter(
                    course_dept=dept).count()

            # List of Departments
            dept_list = Department.objects.all()

            # List of Courses
            course_list = Course.objects.all()

            # List of Department wise Courses
            dept_course_list = {}
            for dept in Department.objects.all():
                dept_course_list[dept.dept_name] = Course.objects.filter(
                    course_dept=dept)

            # List of Staffs
            staff_list = Staff.objects.all()

            # List of Profs
            prof_list = Prof.objects.all()

            context = {
                'student_count': student_count,
                'staff_count': staff_count,
                'prof_count': prof_count,
                'dept_count': dept_count,
                'course_count': course_count,
                'dept_student_count': dept_student_count,
                'course_student_count': course_student_count,
                'dept_course_count': dept_course_count,
                'dept_list': dept_list,
                'course_list': course_list,
                'dept_course_list': dept_course_list,
                'staff_list': staff_list,
                'prof_list': prof_list,
            }

            return render(request, 'admin/admin_home.html', context)
        else:
            return redirect('login')

# ==============Department Related Functions=====================

# Create Department
class Create_dept_view(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '1':
            return render(request, 'admin/admin_create_dept.html')
        else:
            return redirect('login')

class Create_dept(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.user.user_type == '1':
            if request.method == 'POST':
                dept_name = request.POST.get('dept_name')
                dept_uuid = uuid.uuid4()
                dept_code = request.POST.get('dept_code')
                dept_phone = request.POST.get('dept_phone')
                dept_hod = request.POST.get('dept_hod')
                dept_hod_email = request.POST.get('dept_hod_email')

                if dept_name and dept_code and dept_phone and  dept_hod and dept_hod_email :
                    dept = Department.objects.create(
                        dept_name=dept_name,
                        dept_uuid=dept_uuid,
                        dept_code=dept_code,
                        dept_phone=dept_phone,
                        dept_hod=dept_hod,
                        dept_hod_email=dept_hod_email,
                    )
                    messages.success(
                        request, 'Department Created Successfully')
                    return redirect('admin_home')

                else:
                    messages.error(request, 'All Fields are required')
                    return redirect('admin_create_dept_view')
            else:
                return render(request, 'admin/create_dept.html')
        else:
            return redirect('login')

class Manage_dept_view(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '1':
            depts = Department.objects.all()
            context = {
                'department_list': depts,
            }
            return render(request, 'admin/admin_manage_depts.html', context)
        else:
            return redirect('login')

class Edit_dept_view(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, dept_uuid):
        if request.user.user_type == '1':
            dept = Department.objects.get(dept_uuid=dept_uuid)
            context = {
                'dept': dept,
            }
            return render(request, 'admin/admin_edit_dept.html', context)
        else:
            return redirect('login')

class Edit_dept(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, dept_uuid):
        if request.user.user_type == '1':
            if request.method == 'POST':
                # update department
                dept = Department.objects.get(dept_uuid=dept_uuid)
                dept.dept_name = request.POST.get('dept_name')
                dept.dept_code = request.POST.get('dept_code')
                dept.dept_phone = request.POST.get('dept_phone')
                dept.dept_hod = request.POST.get('dept_hod')
                dept.dept_hod_email = request.POST.get('dept_hod_email')
                dept.save()
                messages.success(request, 'Department Updated Successfully')
                return redirect('admin_manage_depts')
            else:
                return render(request, 'admin/admin_manage_depts.html')
        else:
            return redirect('login')

class Delete_dept(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, dept_uuid):
        if request.user.user_type == '1':
            dept = Department.objects.get(dept_uuid=dept_uuid)
            dept.delete()
            messages.success(request, 'Department Deleted Successfully')
            return redirect('admin_manage_depts')
        else:
            return redirect('login')

# ==============Course Related Functions=====================
# Create Course
class Create_course_view(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.user_type == '1':
            depts = Department.objects.all()
            context = {
                'department_list': depts,
            }
            return render(request, 'admin/admin_create_course.html', context)
        else:
            return redirect('login')


class Create_course(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if request.user.user_type == '1':
            course_name = request.POST.get('course_name')
            course_level = request.POST.get('course_level')
            course_dept = request.POST.get('course_dept')
            course_year = request.POST.get('course_year')
            course_sem = request.POST.get('course_sem')
            course_subject_list = request.POST.get('course_subject_list')
            course_subject_credit_list = request.POST.get('course_subject_credit_list')


            if course_name and course_level and course_dept and course_year and course_sem and course_subject_list and course_subject_credit_list:
                course = Course.objects.create(
                    course_name=course_name,
                    course_uuid= uuid.uuid4(),
                    course_level=course_level,
                    course_dept=Department.objects.get(dept_name=course_dept),
                    course_year=course_year,
                    course_sem=course_sem,
                    course_subject_list=course_subject_list,
                    course_subject_credit_list=course_subject_credit_list,
                )
                messages.success(request, 'Course Created Successfully')
                return redirect('admin_home')
            else:
                messages.error(request, 'All Fields are required')
                return redirect('admin_create_course_view')
        else:
            return redirect('login')


class Manage_course_view(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '1':
            courses = Course.objects.all()
            context = {
                'course_list': courses,
            }
            return render(request, 'admin/admin_manage_courses.html', context)
        else:
            return redirect('login')

class Edit_course_view(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, course_uuid):
        if request.user.user_type == '1':
            course = Course.objects.get(course_uuid=course_uuid)
            context = {
                'course': course,
            }
            return render(request, 'admin/admin_edit_course.html', context)
        else:
            return redirect('login')

class Edit_course(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, course_uuid):
        if request.user.user_type == '1':
            if request.method == 'POST':
                # update course
                course = Course.objects.get(course_uuid=course_uuid)
                course.course_name = request.POST.get('course_name')
                course.course_level = request.POST.get('course_level')
                course.course_dept = Department.objects.get(dept_name=request.POST.get('course_dept'))
                course.course_year = request.POST.get('course_year')
                course.course_sem = request.POST.get('course_sem')
                course.course_subject_list = request.POST.get('course_subject_list')
                course.course_subject_credit_list = request.POST.get('course_subject_credit_list')
                course.save()
                messages.success(request, 'Course Updated Successfully')
                return redirect('admin_manage_courses')
            else:
                return render(request, 'admin/admin_manage_courses.html')
        else:
            return redirect('login')

class View_course(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, course_uuid):
        if request.user.user_type == '1':
            course = Course.objects.get(course_uuid=course_uuid)
            subjects = course.course_subject_list.split(',')
            subject_credits = course.course_subject_credit_list.split(',')
            subject_details = []
            for i in range(len(subjects)):
                subject_details.append({'name': subjects[i], 'credit': subject_credits[i]})
            context = {
                'course': course,
                'subject_details': subject_details,
            }
            return render(request, 'admin/admin_view_course.html', context)
        else:
            return redirect('login')

class Delete_course(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, course_uuid):
        if request.user.user_type == '1':
            course = Course.objects.get(course_uuid=course_uuid)
            course.delete()
            messages.success(request, 'Course Deleted Successfully')
            return redirect('admin_manage_courses')
        else:
            return redirect('login')

# ==============Staff Related Functions=====================
# Create Staff
class Create_staff(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if request.user.user_type == '1':
            if request.method == 'POST':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                username = request.POST.get('username')
                email = request.POST.get('email')
                password = request.POST.get('password')
                user = CustomUser.objects.create_user(
                    username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
                user.save()
                messages.success(request, "Staff Added Successfully!")
                return redirect('admin_home')
            else:
                return render(request, 'admin/create_staff.html')
        else:
            return redirect('login')


# ==============Prof Related Functions=====================
# Create Prof
class Create_prof(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if request.method == 'POST':
            if request.user.user_type == '1':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                username = request.POST.get('username')
                email = request.POST.get('email')
                password = request.POST.get('password')
                user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=3)
                user.save()
                messages.success(request, "Prof Added Successfully!")
                return redirect('admin_home')
            else:
                return render('admin/create_prof.html')
        else:
            return render('login')

