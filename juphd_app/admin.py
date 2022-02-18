from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Admin, Prof, Student, Department, StudentResult

# Register your models here.
class UserModel(UserAdmin):
    pass


admin.site.register(CustomUser, UserModel)
admin.site.register(Admin)
admin.site.register(Prof)
admin.site.register(Student)
admin.site.register(Department)
admin.site.register(StudentResult)

