from django.urls import path, include , re_path
from . import views , admin_views , prof_views , student_views
#from users.views import ResetPasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.loginPage, name='login'),
    #path('index/', views.index, name='index'),
    path('doLogin/', views.doLogin, name="doLogin"),
    path('password_reset/', views.ResetPasswordView.as_view(), name="password_reset"),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    path('logout_user/', views.logout_user, name="logout_user"),

    #===================== Admin Views============================
    path('admin_home/', admin_views.Admin_home.as_view(), name="admin_home"),
    path('admin_profile/', admin_views.AdminProfileView.as_view(), name="admin_profile"),
    path('admin_profile_edit/', admin_views.AdminProfileEditView.as_view(), name="admin_profile_edit"),
    path('admin_profile_update/', admin_views.AdminProfileEdit.as_view(), name="admin_profile_update"),

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
    path('admin_create_students/', admin_views.Create_students.as_view(), name="admin_create_students"),
    path('admin_manage_students/', admin_views.Manage_students_view.as_view(), name="admin_manage_students"),
    path('admin_get_dept_profs/', admin_views.Get_department_profs.as_view(), name="admin_get_dept_profs"),
    path('admin_view_student/<student_uuid>/', admin_views.View_student.as_view(), name="admin_view_student"),
    path('admin_edit_student_view/<student_uuid>/', admin_views.Edit_student_view.as_view(), name="admin_edit_student_view"),
    path('admin_edit_student/<student_uuid>/', admin_views.Edit_student.as_view(), name="admin_edit_student"),
    path('admin_delete_student/<student_uuid>/', admin_views.Delete_student.as_view(), name="admin_delete_student"),

    path('admin_student_result_view/', admin_views.Student_result_view.as_view(), name="admin_student_result_view"),
    path('admin_fetch_students/', admin_views.Fetch_students.as_view(), name="admin_fetch_students"),
    path('admin_upload_student_result_view/<student_uuid>', admin_views.Upload_student_result_view.as_view(), name="admin_upload_student_result_view"),
    path('admin_upload_student_result/<student_uuid>', admin_views.Upload_student_result.as_view(), name="admin_upload_student_result"),
    path('admin_view_student_result/<student_uuid>/', admin_views.View_student_result.as_view(), name="admin_view_student_result"),
    path('admin_edit_student_result_view/<student_uuid>/', admin_views.Edit_student_result_view.as_view(), name="admin_edit_student_result_view"),
    path('admin_edit_student_result/<student_uuid>/', admin_views.Edit_student_result.as_view(), name="admin_edit_student_result"),
    path('admin_delete_student_result/<student_uuid>/', admin_views.Delete_student_result.as_view(), name="admin_delete_student_result"),
    path('admin_print_student_data/<student_uuid>/', admin_views.Download_student_data.as_view(), name="admin_print_student_data"),
    
    #===================== Prof Views============================
    path('prof_home/', prof_views.Prof_home.as_view(), name="prof_home"),
    path('prof_profile/', prof_views.ProfProfileView.as_view(), name="prof_profile"),
    path('prof_profile_edit/', prof_views.ProfProfileEditView.as_view(), name="prof_profile_edit"),
    path('prof_profile_update/', prof_views.ProfProfileEdit.as_view(), name="prof_profile_update"),
    path('prof_view_students/', prof_views.ProfStudentListView.as_view(), name="prof_view_students"),
    path('prof_view_student/<student_uuid>/', prof_views.ProfStudentView.as_view(), name="prof_view_student"),
    path('prof_view_student_results/', prof_views.ProfStudentResultListView.as_view(), name="prof_view_student_results"),
    path('prof_view_student_result/<student_uuid>/', prof_views.ProfStudentResultView.as_view(), name="prof_view_student_result"),
    path('prof_print_student_data/<student_uuid>/', prof_views.Download_student_data.as_view(), name="prof_print_student_data"),



    #===================== Student Views============================
    path('student_home/', student_views.Student_home.as_view(), name="student_home"),
    path('student_profile/', student_views.StudentProfileView.as_view(), name="student_profile"),
    path('student_profile_edit/', student_views.studentProfileEditView.as_view(), name="student_profile_edit"),
    path('student_profile_update/', student_views.StudentProfileEdit.as_view(), name="student_profile_update"),
    path('student_view_prof/', student_views.StudentProfView.as_view(), name="student_view_prof"),
    path('student_view_result/', student_views.StudentResultView.as_view(), name="student_view_result"),
    path('student_change_title/', student_views.StudentChangeTitleView.as_view(), name="student_change_title"),


    #===================== Form Validation Views============================
    path('admin_email_check/', admin_views.Email_check.as_view(), name="admin_email_check"),
    path('admin_username_check/', admin_views.Username_check.as_view(), name="admin_username_check"),
]