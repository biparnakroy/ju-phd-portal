from django.urls import path, include
from . import views , admin_views 

urlpatterns = [
    path('', views.loginPage, name='login'),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('password_reset/', views.password_reset, name="password_reset"),
    path('logout_user/', views.logout_user, name="logout_user"),

    #===================== Admin Views============================
    path('admin_home/', admin_views.Admin_home.as_view(), name="admin_home"),

    path('admin_create_dept_view/', admin_views.Create_dept_view.as_view(), name="admin_create_dept_view"),
    path('admin_create_dept/', admin_views.Create_dept.as_view(), name="admin_create_dept"),
    path('admin_manage_depts/', admin_views.Manage_dept_view.as_view(), name="admin_manage_depts"),
    path('admin_edit_dept_view/<dept_uuid>/', admin_views.Edit_dept_view.as_view(), name="admin_edit_dept_view"),
    path('admin_edit_dept/<dept_uuid>/', admin_views.Edit_dept.as_view(), name="admin_edit_dept"),
    path('admin_delete_dept/<dept_uuid>/', admin_views.Delete_dept.as_view(), name="admin_delete_dept"),

    path('admin_create_prof_view/', admin_views.Create_prof_view.as_view(), name="admin_create_prof_view"),
    path('admin_create_prof/', admin_views.Create_prof.as_view(), name="admin_create_prof"),
    path('admin_get_faculty_dept/', admin_views.Get_departments.as_view(), name="admin_get_faculty_dept"),
    path('admin_manage_profs/', admin_views.Manage_prof_view.as_view(), name="admin_manage_profs"),
    path('admin_view_prof/<prof_uuid>/', admin_views.View_prof.as_view(), name="admin_view_prof"),
    path('admin_edit_prof_view/<prof_uuid>/', admin_views.Edit_prof_view.as_view(), name="admin_edit_prof_view"),
    path('admin_edit_prof/<prof_uuid>/', admin_views.Edit_prof.as_view(), name="admin_edit_prof"),
    path('admin_delete_prof/<prof_uuid>/', admin_views.Delete_prof.as_view(), name="admin_delete_prof"),

    path('admin_create_student_view/', admin_views.Create_student_view.as_view(), name="admin_create_student_view"),
    path('admin_create_student/', admin_views.Create_student.as_view(), name="admin_create_student"),
    path('admin_manage_students/', admin_views.Manage_students_view.as_view(), name="admin_manage_students"),
    path('admin_get_dept_profs/', admin_views.Get_department_profs.as_view(), name="admin_get_dept_profs"),
    path('admin_view_student/<student_uuid>/', admin_views.View_student.as_view(), name="admin_view_student"),
    path('admin_edit_student_view/<student_uuid>/', admin_views.Edit_student_view.as_view(), name="admin_edit_student_view"),
    path('admin_edit_student/<student_uuid>/', admin_views.Edit_student.as_view(), name="admin_edit_student"),
    path('admin_delete_student/<student_uuid>/', admin_views.Delete_student.as_view(), name="admin_delete_student"),

    path('admin_student_result_view/', admin_views.Student_result_view.as_view(), name="admin_student_result_view"),
    path('admin_fetch_students/', admin_views.Fetch_students.as_view(), name="admin_fetch_students"),
    path('admin_upload_student_result_view/', admin_views.Upload_student_result_view.as_view(), name="admin_upload_student_result_view"),

    #===================== Form Validation Views============================
    path('admin_email_check/', admin_views.Email_check.as_view(), name="admin_email_check"),
    path('admin_username_check/', admin_views.Username_check.as_view(), name="admin_username_check"),
]