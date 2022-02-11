from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Admin, Prof, Student, Staff, Department, Course, StudentResult

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
admin.site.register(Admin)
admin.site.register(Prof)
admin.site.register(Student)
admin.site.register(Staff)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(StudentResult)

