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

    path('admin_create_course_view/', admin_views.Create_course_view.as_view(), name="admin_create_course_view"),
    path('admin_create_course/', admin_views.Create_course.as_view(), name="admin_create_course"),
    path('admin_manage_courses/', admin_views.Manage_course_view.as_view(), name="admin_manage_courses"),
    path('admin_view_course/<course_uuid>/', admin_views.View_course.as_view(), name="admin_view_course"),
    path('admin_edit_course_view/<course_uuid>/', admin_views.Edit_course_view.as_view(), name="admin_edit_course_view"),
    path('admin_edit_course/<course_uuid>/', admin_views.Edit_course.as_view(), name="admin_edit_course"),
    path('admin_delete_course/<course_uuid>/', admin_views.Delete_course.as_view(), name="admin_delete_course"),

]