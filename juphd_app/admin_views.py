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


# Admin Profile View
class AdminProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        admin = Admin.objects.get(user=request.user)
        context = {
            'admin': admin,
        }
        return render(request, 'admin/admin_profile.html', context)

# Admin Profile Edit View
class AdminProfileEditView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        admin = Admin.objects.get(user=request.user)
        context = {
            'admin': admin,
        }
        return render(request, 'admin/admin_profile_edit.html', context)

# Admin Profile Edit
class AdminProfileEdit(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        admin = Admin.objects.get(user=request.user)
        admin.user.first_name = request.POST['first_name']
        admin.user.last_name = request.POST['last_name']
        admin.user.email = request.POST['email']
        password = request.POST['password']

        # Profile Picture
        if len(request.FILES) != 0:
            profile_pic = request.FILES['profile_pic']
            # uploading profile pic to staff profile pic folder
            extent = profile_pic.name.split('.')[-1]
            filename = 'admin/' + admin.user.first_name+'__'+ admin.user.last_name + '__' + str(uuid.uuid4()) + '.' + extent
            fs = FileSystemStorage()
            filename = fs.save(filename, profile_pic)
            profile_pic_url = fs.url(filename)
            admin.profile_pic = profile_pic_url

         # changing password if not empty
        if password != '':
            # setting new password
            admin.user.set_password(password)
            admin.user.save()
            # re authenticating user with new password and emailbackend
            user = EmailBackEnd.authenticate(request, username=admin.user.email, password=password)
            if user is not None:
                login(request, user)
            else :
                return redirect('login')
            #user = authenticate(username=admin.user.username, password=password)

        admin.user.save()
        admin.save()

        return redirect('admin_profile')


# Admin Home Dashboard
class Admin_home(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.user_type == '1':
            # calculate number of students
            student_count = Student.objects.all().count()
            # calculate number of profs
            prof_count = Prof.objects.all().count()
            # calculate number of Departments
            dept_count = Department.objects.all().count()


            context = {
                'student_count': student_count,
                'prof_count': prof_count,
                'dept_count': dept_count,
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
                dept_faculty = request.POST.get('dept_faculty')
                dept_hod = request.POST.get('dept_hod')
                dept_hod_email = request.POST.get('dept_hod_email')

                if dept_name and dept_code and dept_phone and  dept_hod and dept_hod_email and dept_faculty:
                    dept = Department.objects.create(
                        dept_name=dept_name,
                        dept_faculty=dept_faculty,
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
                dept.dept_faculty = request.POST.get('dept_faculty')
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

# ==============Prof Related Functions=====================
# Create Prof View
class Create_prof_view(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.user_type == '1':
            departments = Department.objects.all()
            context = {
                'departments': departments,
            }
            return render(request, 'admin/admin_create_prof.html', context)
        else:
            return redirect('login')


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
                department = request.POST.get('department')
                prof_faculty = request.POST.get('prof_faculty')
                password = request.POST.get('password')

                if len(request.FILES) != 0:
                    profile_pic = request.FILES['profile_pic']
                    # uploading profile pic to staff profile pic folder
                    extent = profile_pic.name.split('.')[-1]
                    filename = 'prof/' + first_name+'__'+last_name + '__' + str(uuid.uuid4()) + '.' + extent
                    fs = FileSystemStorage()
                    filename = fs.save(filename, profile_pic)
                    profile_pic_url = fs.url(filename)
                else:
                    profile_pic_url = "/media/staff/user.png"


                if first_name and last_name and username and email and password and department:
                    user = CustomUser.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name, user_type=2)
                    user.prof.profile_pic = profile_pic_url
                    print(department)
                    user.prof.prof_dept = Department.objects.get(dept_uuid=department)
                    user.prof.prof_faculty = prof_faculty
                    user.prof.prof_uuid = uuid.uuid4()
                    user.save()
                    messages.success(request, 'Professor Created Successfully')
                    return redirect('admin_home')
                else:
                    messages.error(request, 'All Fields are required')
                    return redirect('admin_create_prof_view')

                messages.success(request, "Prof Added Successfully!")
                return redirect('admin_home')
            else:
                return render('admin/admin_create_prof.html')
        else:
            return render('login')

# Manage Profs View
class Manage_prof_view(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.user_type == '1':
            profs = CustomUser.objects.filter(user_type=2)
            context = {
                'prof_list': profs,
            }
            return render(request, 'admin/admin_manage_profs.html', context)
        else:
            return redirect('login')

# Edit Prof View
class Edit_prof_view(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, prof_uuid):
        if request.user.user_type == '1':
            prof = Prof.objects.get(prof_uuid=prof_uuid)
            prof_custom_user = CustomUser.objects.get(id=prof.user_id)
            departments = Department.objects.all()
            context = {
                'departments': departments,
                'prof': prof_custom_user,
            }
            return render(request, 'admin/admin_edit_prof.html', context)
        else:
            return redirect('login')


# Edit Prof
class Edit_prof(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, prof_uuid):
        if request.method == 'POST':
            if request.user.user_type == '1':
                prof = Prof.objects.get(prof_uuid=prof_uuid)
                prof_custom_user = CustomUser.objects.get(id=prof.user_id)
                try:
                    prof_custom_user.first_name = request.POST.get('first_name')
                    prof_custom_user.last_name = request.POST.get('last_name')
                    prof_custom_user.username = request.POST.get('username')
                    prof_custom_user.email = request.POST.get('email')
                    prof_custom_user.prof.prof_dept = Department.objects.get(dept_name=request.POST.get('department'))
                    new_password = request.POST.get('password')
                    if new_password:
                        prof_custom_user.set_password(new_password)
                    if len(request.FILES) != 0:
                        profile_pic = request.FILES['profile_pic']
                        # uploading profile pic to staff profile pic folder
                        extent = profile_pic.name.split('.')[-1]
                        filename = 'prof/' + prof_custom_user.first_name+'__'+prof_custom_user.last_name + '__' + str(uuid.uuid4()) + '.' + extent
                        fs = FileSystemStorage()
                        filename = fs.save(filename, profile_pic)
                        profile_pic_url = fs.url(filename)
                        prof_custom_user.prof.profile_pic = profile_pic_url
                except:
                    pass

                prof_custom_user.save()
                prof_custom_user.prof.save()

                messages.success(request, 'Staff Updated Successfully')
                return redirect('admin_manage_profs')
            else:
                return render(request, 'admin/admin_manage_profs.html')
        else:
            return redirect('login')

# View Prof
class View_prof(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, prof_uuid):
        if request.user.user_type == '1':
            prof = Prof.objects.get(prof_uuid=prof_uuid)
            prof_custom_user = CustomUser.objects.get(id=prof.user_id)
            context = {
                'prof': prof_custom_user,
            }
            return render(request, 'admin/admin_view_prof.html', context)
        else:
            return redirect('login')

# Delete Prof
class Delete_prof(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, prof_uuid):
        if request.user.user_type == '1':
            prof = Prof.objects.get(prof_uuid=prof_uuid)
            prof_id = prof.user_id
            prof_custom_user = CustomUser.objects.get(id=prof_id)
            # deleting the profile pic
            # if prof.profile_pic:
            #     fs = FileSystemStorage()
            #     profile_pic_url = prof.profile_pic
            #     fs.delete(profile_pic_url)
            
            prof.delete()
            prof_custom_user.delete()
            messages.success(request, 'Professor Deleted Successfully')
            return redirect('admin_manage_profs')
        else:
            return redirect('login')

# Get departments of a faculty
class Get_departments(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if request.user.user_type == '1':
            faculty = request.POST.get('faculty')
            departments = Department.objects.filter(dept_faculty=faculty)
            department_list = []
            for department in departments:
                dept = {
                    'dept_uuid': department.dept_uuid,
                    'dept_name': department.dept_name,
                }
                department_list.append(dept)
            return JsonResponse(department_list, safe=False)
        else:
            return redirect('login')


#=====================Student Related Functions====================
# Create Student View
class Create_student_view(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.user_type == '1':
            departments = Department.objects.all()
            professors = CustomUser.objects.filter(user_type=3)
            context = {
                'departments': departments,
                'professors': professors,
            }
            return render(request, 'admin/admin_create_student.html', context)
        else:
            return redirect('login')

# Create Student
class Create_students(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if request.method == 'POST':
            if request.user.user_type == '1':
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                username = request.POST.get('username')
                email = request.POST.get('email')

                index_no = request.POST.get('index_no')
                student_faculty = request.POST.get('student_faculty')
                student_date_of_reg = request.POST.get('student_date_of_reg')
                student_category = request.POST.get('student_category')
                if request.POST.get('student_scholarship'):
                    student_scholarship = request.POST.get('student_scholarship')
                else:
                    student_scholarship = 'No'
                department = request.POST.get('department')
                prof_under = request.POST.get('prof_under')
                title_of_thesis = request.POST.get('title_of_thesis')
                pre_thesis_submission_date = request.POST.get('pre_thesis_submission_date')
                defence = request.POST.get('defence_date')
                password = request.POST.get('student_password')

                try:
                    profile_pic = request.FILES['profile_pic']
                    # uploading profile pic to student profile pic folder
                    extent = profile_pic.name.split('.')[-1]
                    filename = 'student/' + first_name+'__'+last_name + '__' + str(uuid.uuid4()) + '.' + extent
                    fs = FileSystemStorage()
                    filename = fs.save(filename, profile_pic)
                    profile_pic_url = fs.url(filename)
                except:
                    profile_pic_url = "/media/student/user.png"

                # checking if research paper is submitted
                try:
                    thesis_review_paper_1 = request.FILES['thesis_review_paper_1']
                    fs = FileSystemStorage()
                    # uploading thesis review paper to student thesis review paper folder
                    extent = thesis_review_paper_1.name.split('.')[-1]
                    filename ='papers/'+first_name+'__'+last_name + '__' + str(uuid.uuid4()) + '.' + extent
                    filename = fs.save(filename, thesis_review_paper_1)
                    thesis_review_paper_1_url = fs.url(filename)
                except:
                    thesis_review_paper_1_url = None

                try:
                    thesis_review_paper_2 = request.FILES['thesis_review_paper_2']
                    fs = FileSystemStorage()
                    # uploading thesis review paper to student thesis review paper folder
                    extent = thesis_review_paper_2.name.split('.')[-1]
                    filename ='papers/'+first_name+'__'+last_name + '__' + str(uuid.uuid4()) + '.' + extent
                    filename = fs.save(filename, thesis_review_paper_2)
                    thesis_review_paper_2_url = fs.url(filename)
                except:
                    thesis_review_paper_2_url = None

                
                    
                # making the user
                if first_name and last_name and username and email and index_no and student_category and student_scholarship and department and prof_under and title_of_thesis and pre_thesis_submission_date and defence and password and student_faculty:
                    student = CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, user_type=3)
                    student.student.student_faculty = student_faculty
                    student.student.index_no = index_no
                    student.student.student_date_of_reg = student_date_of_reg
                    student.student.student_category = student_category
                    student.student.student_scholarship = student_scholarship
                    student.student.student_department = Department.objects.get(dept_uuid=department)
                    student.student.prof_under = Prof.objects.get(prof_uuid=prof_under)
                    student.student.title_of_thesis = title_of_thesis
                    student.student.pre_thesis_submission_date = pre_thesis_submission_date
                    student.student.defence = defence
                    student.student.profile_pic = profile_pic_url
                    student.student.thesis_review_paper_1 = thesis_review_paper_1_url
                    student.student.thesis_review_paper_2 = thesis_review_paper_2_url
                    student.save()
                    student.student.save()
                    messages.success(request, 'Student Created Successfully')
                    return redirect('admin_manage_students')
                else:
                    messages.error(request, 'Please fill all the fields')
                    print("fill all the fields")
                    return redirect('admin_create_student_view')
            else:
                return redirect('login')
        else:
            print('error')
            return redirect('admin_create_students_view')
            



# Get department professors
class Get_department_profs(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if request.user.user_type == '1':
            department = request.POST.get('department')
            professors = CustomUser.objects.filter(user_type=2, prof__prof_dept=Department.objects.get(dept_uuid=department))
            professors_list = []
            for prof in professors:
                professors_list.append({
                    'prof_uuid': prof.prof.prof_uuid,
                    'first_name': prof.first_name,
                    'last_name': prof.last_name,
                })
            return JsonResponse(professors_list, safe=False)
        else:
            return redirect('login')

# Manage Students View
class Manage_students_view(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.user_type == '1':
            students = CustomUser.objects.filter(user_type=3)
            context = {
                'students': students,
            }
            return render(request, 'admin/admin_manage_students.html', context)
        else:
            return redirect('login')


# View Student
class View_student(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, student_uuid):
        if request.user.user_type == '1':
            student = Student.objects.get(student_uuid=student_uuid)
            context = {
                'student': student,
            }
            return render(request, 'admin/admin_view_student.html', context)
        else:
            return redirect('login')

# Edit Student View
class Edit_student_view(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, student_uuid):
        if request.user.user_type == '1':
            student = Student.objects.get(student_uuid=student_uuid)
            departments = Department.objects.all()
            context = {
                'student': student,
                'departments': departments,
            }
            return render(request, 'admin/admin_edit_student.html', context)
        else:
            return redirect('login')

# Edit Student
class Edit_student(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, student_uuid):
        if request.method == 'POST':
            if request.user.user_type == '1':
                student = Student.objects.get(student_uuid=student_uuid)
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                username = request.POST.get('username')
                email = request.POST.get('email')
                student_category = request.POST.get('student_category')
                student_scholarship = request.POST.get('student_scholarship')
                student_faculty = request.POST.get('student_faculty')
                student_department = request.POST.get('department')
                prof_under = request.POST.get('prof_under')
                index_no= request.POST.get('index_no')
                date_of_reg = request.POST.get('student_date_of_reg')
                title_of_thesis = request.POST.get('title_of_thesis')
                pre_thesis_submission_date = request.POST.get('pre_thesis_submission_date')
                defence = request.POST.get('defence_date')  
                password = request.POST.get('student_password')

                try:
                    profile_pic = request.FILES['profile_pic']
                    # uploading profile pic to student profile pic folder
                    extent = profile_pic.name.split('.')[-1]
                    filename = 'student/' + first_name+'__'+last_name + '__' + str(uuid.uuid4()) + '.' + extent
                    fs = FileSystemStorage()
                    filename = fs.save(filename, profile_pic)
                    profile_pic_url = fs.url(filename)
                except:
                    profile_pic_url = student.profile_pic

                 # checking if research paper is submitted
                try:
                    thesis_review_paper_1 = request.FILES['thesis_review_paper_1']
                    fs = FileSystemStorage()
                    # uploading thesis review paper to student thesis review paper folder
                    extent = thesis_review_paper_1.name.split('.')[-1]
                    filename ='papers/'+first_name+'__'+last_name + '__' + str(uuid.uuid4()) + '.' + extent
                    filename = fs.save(filename, thesis_review_paper_1)
                    thesis_review_paper_1_url = fs.url(filename)
                except:
                    thesis_review_paper_1_url = student.thesis_review_paper_1

                try:
                    thesis_review_paper_2 = request.FILES['thesis_review_paper_2']
                    fs = FileSystemStorage()
                    # uploading thesis review paper to student thesis review paper folder
                    extent = thesis_review_paper_2.name.split('.')[-1]
                    filename ='papers/'+first_name+'__'+last_name + '__' + str(uuid.uuid4()) + '.' + extent
                    filename = fs.save(filename, thesis_review_paper_2)
                    thesis_review_paper_2_url = fs.url(filename)
                except:
                    thesis_review_paper_2_url = student.thesis_review_paper_2

                # print(first_name)
                # print(last_name)
                # print(username)
                # print(email)
                # print(student_category)
                # print(student_scholarship)
                # print(student_faculty)
                # print(student_department)
                # print(prof_under)
                # print(index_no)
                # print(date_of_reg)
                # print(title_of_thesis)
                # print(pre_thesis_submission_date)
                # print(defence)
                

                if first_name and last_name and username and email and student_category and student_scholarship and student_faculty and student_department and prof_under and index_no and date_of_reg and title_of_thesis and pre_thesis_submission_date and defence:
                    student.user.first_name = first_name
                    student.user.last_name = last_name
                    student.user.email = email
                    student.user.username = username
                    if password:
                        student.user.set_password(password)
                    student.user.save()
                    student.student_category = student_category
                    student.student_scholarship = student_scholarship
                    student.student_faculty = student_faculty
                    student.student_department = Department.objects.get(dept_uuid=student_department)
                    student.prof_under = Prof.objects.get(prof_uuid=prof_under)
                    student.index_no = index_no
                    student.student_date_of_reg = date_of_reg
                    student.title_of_thesis = title_of_thesis
                    student.pre_thesis_submission_date = pre_thesis_submission_date
                    student.defence = defence
                    student.thesis_review_paper_1 = thesis_review_paper_1_url
                    student.thesis_review_paper_2 = thesis_review_paper_2_url
                    student.profile_pic = profile_pic_url
                    student.save()
                    messages.success(request, 'Student Updated Successfully')
                    return redirect('admin_home')
                else:
                    print('error')
                    messages.error(request, 'All Fields are required')
                    return redirect('admin_edit_student_view', student_uuid)
            else:
                return redirect('login')
        else:
            return redirect('login')
    
        
# Delete Student
class Delete_student(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, student_uuid):
        if request.user.user_type == '1':
            student = Student.objects.get(student_uuid=student_uuid)
            student_id = student.user_id
            student_custom_user = CustomUser.objects.get(id=student_id)
            # deleting the profile pic
            # if student.profile_pic:
            #     fs = FileSystemStorage()
            #     profile_pic_url = student.profile_pic
            #     fs.delete(profile_pic_url)
            
            student.delete()
            student_custom_user.delete()
            messages.success(request, 'Student Deleted Successfully')
            return redirect('admin_manage_students')
        else:
            return redirect('login')

#=====================Student Result Views=====================

# Student Result View
class Student_result_view(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        if request.user.user_type == '1':
            faculty = ["Engineering", "Science", "Arts", "Interdisciplinary"]
            context = {
                'faculty': faculty,
            }
            return render(request, 'admin/admin_student_result.html', context)
        else:
            return redirect('login')

# Fetch Students
class Fetch_students(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if request.method == 'POST':
            if request.user.user_type == '1':
                faculty = ["Engineering", "Science", "Arts", "Interdisciplinary"]
                query_faculty = request.POST.get('faculty')
                department = request.POST.get('department')
                students = Student.objects.filter(student_faculty=query_faculty, student_department=Department.objects.get(dept_uuid=department))
                students_list = []
                for student in students:
                    student_result_exists = StudentResult.objects.filter(student_result_student=student).exists()

                    student_details = {
                        'student_uuid': student.student_uuid,
                        'first_name': student.user.first_name,
                        'last_name': student.user.last_name,
                        'username': student.user.username,
                        'email': student.user.email,
                        'student_category': student.student_category,
                        'student_scholarship': student.student_scholarship,
                        'student_faculty': student.student_faculty,
                        'student_department': student.student_department.dept_name,
                        'prof_under': student.prof_under.user.first_name + ' ' + student.prof_under.user.last_name,
                        'index_no': student.index_no,
                        'student_date_of_reg': student.student_date_of_reg,
                        'title_of_thesis': student.title_of_thesis,
                        'pre_thesis_submission_date': student.pre_thesis_submission_date,
                        'defence': student.defence,
                        'student_result_exists': student_result_exists,
                    }
                    students_list.append(student_details)
                return JsonResponse(students_list, safe=False)
            else:
                return redirect('login')
        else:
            return redirect('admin_student_result_view')

# Upload Student Result View
class Upload_student_result_view(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, student_uuid):
        if request.method == 'GET':
            if request.user.user_type == '1':
                student = Student.objects.get(student_uuid=student_uuid)
                context = {
                    'student': student,
                }
                return render(request, 'admin/admin_upload_student_result_view.html', context)
                messages.success(request, 'Student Result Uploaded Successfully')
            else:
                return redirect('login')
        else:
            return redirect('login')

# Upload Student Result
class Upload_student_result(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, student_uuid):
        if request.method == 'POST':
            if request.user.user_type == '1':
                student = Student.objects.get(student_uuid=student_uuid)
                student_result_id = uuid.uuid4()
                student_result_student = student
                student_result_paper_1_number = request.POST.get('paper_1_number')
                student_result_paper_2_number = request.POST.get('paper_2_number')

                # creating the student result
                if student_result_paper_1_number and student_result_paper_2_number:
                    student_result = StudentResult(
                        student_result_id=student_result_id,
                        student_result_student=student_result_student,
                        student_result_paper_1_number=student_result_paper_1_number,
                        student_result_paper_2_number=student_result_paper_2_number,
                    )
                    student_result.save()

                    messages.success(request, 'Student Result Uploaded Successfully')
                    return redirect('admin_view_student_result', student_uuid)
                else:
                    messages.error(request, 'All Fields are required')
                    return redirect('admin_upload_student_result', student_uuid)

                return redirect('admin_student_result_view')

            else:
                return redirect('login')
        else:
            return redirect('login')


# Edit Student Result View
class Edit_student_result_view(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, student_uuid):
        if request.method == 'GET':
            if request.user.user_type == '1':
                student = Student.objects.get(student_uuid=student_uuid)
                student_result = StudentResult.objects.get(student_result_student=student)
                context = {
                    'student': student,
                    'student_result': student_result,
                }
                return render(request, 'admin/admin_edit_student_result_view.html', context)
            else:
                return redirect('login')
        else:
            return redirect('login')

# Edit Student Result
class Edit_student_result(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, student_uuid):
        if request.method == 'POST':
            if request.user.user_type == '1':
                student = Student.objects.get(student_uuid=student_uuid)
                student_result = StudentResult.objects.get(student_result_student=student)
                student_result_paper_1_number = request.POST.get('paper_1_number')
                student_result_paper_2_number = request.POST.get('paper_2_number')

                # creating the student result
                if student_result_paper_1_number and student_result_paper_2_number:
                    student_result.student_result_paper_1_number = student_result_paper_1_number
                    student_result.student_result_paper_2_number = student_result_paper_2_number
                    student_result.save()
                    messages.success(request, 'Student Result Updated Successfully')
                    return redirect('admin_view_student_result', student_uuid)
                else:
                    messages.error(request, 'All Fields are required')
                    return redirect('admin_edit_student_result', student_uuid)

                return redirect('admin_student_result_view')

            else:
                return redirect('login')
        else:
            return redirect('login')


# View Student Result
class View_student_result(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, student_uuid):
        if request.method == 'GET':
            if request.user.user_type == '1':
                student = Student.objects.get(student_uuid=student_uuid) 
                student_result = StudentResult.objects.get(student_result_student=student)
                if student_result:
                    context = {
                        'student': student,
                        'student_result': student_result,
                    }
                    return render(request, 'admin/admin_view_student_result.html', context)
                else:
                    messages.error(request, 'Student Result Not Found')
                    return redirect('admin_student_result_view')
            else:
                return redirect('login')
        else:
            return redirect('login')


# Delete Student Result
class Delete_student_result(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, student_uuid):
        if request.user.user_type == '1':
            student = Student.objects.get(student_uuid=student_uuid)
            student_result = StudentResult.objects.get(student_result_student=student)
            student_result.delete()
            messages.success(request, 'Student Result Deleted Successfully')
            return redirect('admin_student_result_view')
        else:
            return redirect('login')

#=====================Form Validation Function=====================

#checking if the username is already taken
class Username_check(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if request.user.user_type == '1':
            username = request.POST.get('username')
            user = CustomUser.objects.filter(username=username).exists()
            if user:
                return JsonResponse({'status': 'taken'})
            else:
                return JsonResponse({'status': 'available'})
        else:
            return redirect('login')

#checking if the email is already taken
class Email_check(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        if request.user.user_type == '1':
            email = request.POST.get('email')
            user = CustomUser.objects.filter(email=email).exists()
            if user:
                return JsonResponse({'status': 'taken'})
            else:
                return JsonResponse({'status': 'available'})
        else:
            return redirect('login')
