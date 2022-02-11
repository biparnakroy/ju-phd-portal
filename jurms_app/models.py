from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
import uuid

#========= Department Course =========

class Department(models.Model):
    dept_name = models.CharField(max_length=100)
    dept_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    dept_code = models.CharField(max_length=100, unique=True)
    dept_phone = models.CharField(max_length=100, blank=True, null=True)
    dept_hod = models.CharField(max_length=100, blank=True)
    dept_hod_email = models.EmailField(max_length=100, blank=True)

class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)
    course_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    course_level = models.CharField(max_length=100)
    course_dept = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_year = models.CharField(max_length=100)
    course_sem = models.CharField(max_length=100)
    course_subject_list = models.TextField()
    course_subject_credit_list = models.TextField()

#=========== User Model ===========
class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"Staff"),(3,"Prof"),(4,"Student"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class Admin(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    admin_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Staff(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    staff_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Prof(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    prof_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Student(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    student_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    roll_no=models.CharField(max_length=10)
    email=models.EmailField(max_length=254)
    prof_under=models.ForeignKey(Prof,on_delete=models.CASCADE)
    student_department=models.ForeignKey(Department,on_delete=models.CASCADE)
    student_course_list=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#========== Student Result ===========
class StudentResult(models.Model):
    student_result_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_result_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_result_course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_course_result = models.TextField()
    student_result_created_at = models.DateTimeField(auto_now_add=True)
    student_result_updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


#============= Creating signals ============
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type==1:
            Admin.objects.create(user=instance)
        if instance.user_type==2:
            Staff.objects.create(user=instance)
        if instance.user_type==3:
            Prof.objects.create(user=instance)
        if instance.user_type==4:
            Student.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.prof.save()
    if instance.user_type == 4:
        instance.student.save()


