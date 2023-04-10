import subprocess,pytz,json
from datetime import datetime
from django.db.models import Count,Q
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from ams_app.models import CustomUser, Staffs, Students, Subjects, Timetable, Courses, AttendanceLog, AttendanceReport, LeaveReportStaff, LeaveReportStudent, FeedBackStaffs, FeedBackStudent
User = get_user_model()

def staff_home(request):
    
    student_count1=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.filter(staff_id=request.user.id).count()

    staff_obj=CustomUser.objects.get(id=request.user.id)
    current_staff = staff_obj
    total_lectures1 = AttendanceReport.objects.filter(
        Q(subject__staff=current_staff) & ~Q(attendance=None)
    ).values('subject').distinct().count()
    
    subjects_all=Subjects.objects.all()
    subject_list=[]
    for subject in subjects_all:
        subject_list.append(subject.subject_name)
    for subject in subjects_all:
        subject_list.append(subject.subject_name)
        students_all=Students.objects.all()
        attendance_present_list_student=[]
        attendance_absent_list_student=[]
        student_name_list=[]
        for student in students_all:
            attendance=AttendanceReport.objects.filter(student_id=student.id,status="Present").count()
            absent=AttendanceReport.objects.filter(student_id=student.id,status="Absent").count()
            attendance_present_list_student.append(attendance)
            attendance_absent_list_student.append(absent)
            student_name_list.append(student.admin.username)
         
    return render(request,"staff_templates/staff_home.html",{"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"subject_list":subject_list,'total_lectures':total_lectures1,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student})



def view_attendance(request):
    subjects=Subjects.objects.all()
    return render (request,"staff_templates/staff_view_attendance.html",{"subjects":subjects})

def attendance_report(request):
    subject_id = request.GET.get('subject_id')
    date1=request.GET.get('date')
    date_obj = datetime.strptime(date1, '%d %B %Y')
    date2 = date_obj.strftime('%Y-%m-%d')
    attendance_reports = AttendanceReport.objects.filter(subject_id=subject_id,created_at__date=date2)
    attendance_data = []
    for report in attendance_reports:
        status = report.status
        student_name = User.objects.get(id=report.student.admin_id).first_name
        attendance_data.append({ 'status': status, 'student_name': student_name})
    response_data = {'attendance_data': attendance_data}
    return JsonResponse(response_data)

def staff_apply_leave(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    leave_data=LeaveReportStaff.objects.filter(staff_id=staff_obj)
    return render(request,"staff_templates/staff_apply_leave.html",{"leave_data":leave_data})

def staff_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("/staff_apply_leave")
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        staff_obj=Staffs.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStaff(staff_id=staff_obj.id,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect("/staff_apply_leave")
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect("/staff_apply_leave")


def staff_feedback(request):
    staff_id=Staffs.objects.get(admin=request.user.id)
    feedback_data=FeedBackStaffs.objects.filter(staff_id=staff_id)
    return render(request,"staff_templates/staff_feedback.html",{"feedback_data":feedback_data})

def staff_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("staff_feedback_save")
    else:
        feedback_msg=request.POST.get("feedback_msg")

        staff_obj=Staffs.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStaffs(staff_id=staff_obj.id,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect("/staff_give_feedback")
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect("/staff_give_feedback")
    
