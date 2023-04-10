"""ams URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ams_app import views
from ams_app import adminview,staffview,studentview
from django.conf.urls.static import static
from ams import settings

urlpatterns = [
    path('',views.showLoginPage),
    path('admin/', admin.site.urls),
    path('doLogin',views.doLogin),
    path('get_user_details',views.GetUserDetails),
    path('logout_user',views.logout_user),
    path('admin_home',adminview.admin_home),
    path('manage_timetable',adminview.manage_timetable),
    path('add_lecture',adminview.add_lecture),
    path('add_lecture_save',adminview.add_lecture_save),
    path('add_staff',adminview.add_staff),
    path('add_staff_save',adminview.add_staff_save),
    path('add_student',adminview.add_student),
    path('add_student_save',adminview.add_student_save),
    path('add_subject',adminview.add_subject),
    path('add_subject_save',adminview.add_subject_save),
    path('manage_staff',adminview.manage_staff),
    path('manage_student',adminview.manage_student),
    path('manage_subject',adminview.manage_subject),
    path('edit_staff/<str:staff_id>',adminview.edit_staff),
    path('edit_staff_save',adminview.edit_staff_save),
    path('edit_student/<str:student_id>',adminview.edit_student),
    path('edit_subject/<str:subject_id>', adminview.edit_subject),
    path('edit_subject_save', adminview.edit_subject_save),
    path('edit_student_save',adminview.edit_student_save),
    path('edit_lecture/<str:timetable_id>',adminview.edit_lecture),
    path('edit_lecture_save',adminview.edit_lecture_save),
    path('delete_staff/<str:staff_id>/', adminview.delete_staff),
    path('delete_student/<str:student_id>/', adminview.delete_student),
    path('delete_subject/<str:subject_id>/', adminview.delete_subject),
    path('delete_lecture/<str:timetable_id>/', adminview.delete_lecture),
    path('student_leave_view', adminview.student_leave_view),
    path('staff_leave_view', adminview.staff_leave_view),
    path('student_approve_leave/<str:leave_id>', adminview.student_approve_leave),
    path('student_disapprove_leave/<str:leave_id>', adminview.student_disapprove_leave),
    path('staff_approve_leave/<str:leave_id>', adminview.staff_approve_leave),
    path('staff_disapprove_leave/<str:leave_id>', adminview.staff_disapprove_leave),
    path('student_feedback', adminview.student_feedback,name="student_feedback_message"),
    path('student_feedback_message_replied', adminview.student_feedback_message_replied,name="student_feedback_message_replied"),
    path('staff_feedback', adminview.staff_feedback,name="staff_feedback_message"),
    path('staff_feedback_message_replied', adminview.staff_feedback_message_replied,name="staff_feedback_message_replied"),
    path('view_attendance',adminview.view_attendance),
    path('attendance_report', adminview.attendance_report, name='attendance_report'),
   
    

    path('staff_home', staffview.staff_home, name="staff_home"),
    path('staff_view_attendance',staffview.view_attendance),
    path('staff_attendance_report', staffview.attendance_report, name='staff_attendance_report'),
    path('staff_apply_leave', staffview.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', staffview.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_give_feedback', staffview.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', staffview.staff_feedback_save, name="staff_feedback_save"),
    
    path('student_home', studentview.student_home, name="student_home"),
    path('student_view_attendance', studentview.view_attendance),
    path('student_attendance_report', studentview.attendance_report, name='student_attendance_report'),
    path('student_apply_leave', studentview.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', studentview.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_give_feedback', studentview.student_feedback, name="student_feedback"),
    path('student_feedback_save', studentview.student_feedback_save, name="student_feedback_save"),
    path('scan_barcode', studentview.run_script, name='scan_barcode'),
    path('submit_attendance', studentview.perform_operation, name='submit_attendance'),
    path('mark_attendance',studentview.test, name='mark_attendance'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)

