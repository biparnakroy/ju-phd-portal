from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser
import uuid

#========= Department Course =========

class Department(models.Model):
    dept_name = models.CharField(max_length=100)
    dept_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    dept_faculty = models.CharField(max_length=100,null=True,blank=True)
    dept_code = models.CharField(max_length=100, unique=True)
    dept_phone = models.CharField(max_length=100, blank=True, null=True)
    dept_hod = models.CharField(max_length=100, blank=True)
    dept_hod_email = models.EmailField(max_length=100, blank=True)

    def __str__(self):
        return self.dept_name


#=========== User Model ===========
class CustomUser(AbstractUser):
    user_type_data=((1,"Admin"),(2,"Prof"),(3,"Student"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

class Admin(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    admin_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    profile_pic = models.FileField(default="/media/admin/user.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Prof(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    prof_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    prof_dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, default=None)
    prof_faculty = models.CharField(max_length=100, blank=True)
    profile_pic = models.FileField(default="/media/prof/user.png")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Student(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    student_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    profile_pic = models.FileField(default="/media/student/user.png")
    student_date_of_reg = models.DateField(null=True,blank=True)
    index_no=models.CharField(max_length=12,unique=True)
    student_faculty = models.CharField(max_length=100, blank=True)
    student_category=models.CharField(max_length=100,blank=True)
    student_scholarship=models.CharField(max_length=100,blank=True)
    student_department=models.ForeignKey(Department,on_delete=models.CASCADE, null=True)
    prof_under=models.ForeignKey(Prof,on_delete=models.CASCADE, null=True)
    title_of_thesis=models.CharField(max_length=200,blank=True)
    pre_thesis_submission_date=models.DateField(null=True,blank=True)
    defence = models.DateField(null=True,blank=True)
    thesis_review_paper_1 = models.FileField(null=True,blank=True)
    thesis_review_paper_2 = models.FileField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

#========== Student Result ===========
class StudentResult(models.Model):
    student_result_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student_result_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_result_paper_1_number = models.CharField(max_length=100, blank=True)
    student_result_paper_2_number = models.CharField(max_length=100, blank=True)
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
            Prof.objects.create(user=instance)
        if instance.user_type==3:
            Student.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.prof.save()
    if instance.user_type == 3:
        instance.student.save()


