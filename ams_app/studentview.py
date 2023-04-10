import subprocess,pytz,json
from datetime import datetime
from django.db.models import Count
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
User=get_user_model()
from ams_app.models import CustomUser, Staffs, Students, Subjects, Timetable, Courses, AttendanceLog, AttendanceReport, LeaveReportStaff, LeaveReportStudent, FeedBackStaffs, FeedBackStudent
def student_home(request):
    student_obj=Students.objects.get(admin=request.user.id)
    attendance_total=AttendanceReport.objects.filter(student_id=student_obj).count()
    attendance_present=AttendanceReport.objects.filter(student_id=student_obj,status=True).count()
    attendance_absent=AttendanceReport.objects.filter(student_id=student_obj,status=False).count()
    course=Courses.objects.get(id=1)
    subjects=Subjects.objects.filter(course_id=course).count()
    subjects_data=Subjects.objects.filter(course_id=1)
    
    subjects_all=Subjects.objects.all()
    subject_list=[]
    for subject in subjects_all:
        subject_list.append(subject.subject_name)
    for subject in subjects_all:
        subject_list.append(subject.subject_name)
        students_all=student_obj
        attendance_present_list_student=[]
        attendance_absent_list_student=[]
        student_name_list=[]
        attendance=AttendanceReport.objects.filter(student_id=student_obj.id,status="Present").count()
        absent=AttendanceReport.objects.filter(student_id=student_obj.id,status="Absent").count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(absent)
        student_name_list.append(student_obj.admin.username)
    return render(request,"student_templates/student_home.html",{"total_attendance":attendance_total,"attendance_absent":attendance_absent,"attendance_present":attendance_present,"subjects":subjects,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student[0],"attendance_absent_list_student":attendance_absent_list_student[0],"subject_list":subject_list})


def view_attendance(request):
    subjects=Subjects.objects.all()
    return render (request,"student_templates/student_view_attendance.html",{"subjects":subjects})


def attendance_report(request):
    user = request.user
    student_id = user.students.id
    date1 = request.GET.get('date')
    subject_id=request.GET.get('subject_id')
    date_obj = datetime.strptime(date1, '%d %B %Y')
    date2 = date_obj.strftime('%Y-%m-%d')
    attendance_reports = AttendanceReport.objects.filter(student_id=student_id, created_at__date=date2,subject_id=subject_id)
    attendance_data = []
    for report in attendance_reports:
        status = report.status
        student_name = user.first_name
        attendance_data.append({ 'status': status, 'student_name': student_name})
    response_data = {'attendance_data': attendance_data}
    return JsonResponse(response_data)

def get_student_id(card_number):

    # Retrieve the student id from the Students table based on the card number
    try:
        student = Students.objects.get(card_number=card_number)
        return student.id
    except Students.DoesNotExist:
        return None

def run_script(request):
    if request.method=='POST':
        result = subprocess.run(['python3', '/home/omesh/notes/python_lab/project/ok.py'],stdout=subprocess.PIPE, universal_newlines=True)
        output = result.stdout
        dictionary = eval(output)
        table_html = '<table><thead><tr><th>Attribute</th><th>Value</th></tr></thead><tbody>'
        for key, value in dictionary.items():
            if key == 'barcode':
                student_id = get_student_id(value)
                if student_id is not None:
                    table_html += '<tr><td>student_id</td><td>{}</td></tr>'.format(student_id)
            table_html += '<tr><td>{}</td><td>{}</td></tr>'.format(key, value)
        table_html += '</tbody></table>'
        return HttpResponse(table_html)

def perform_operation(request):
    user_id = request.user.id
    student = Students.objects.get(admin_id=user_id)
    student_table_id=student.id
    if request.method == 'POST':
        value1 = request.POST.get('student_id')
        value2 = request.POST.get('timestamp')
        value3 = request.POST.get('day')
        if value1 == str(student_table_id):
            attendance_log = AttendanceLog(scan_time=value2,student_id=value1, day=value3)
            attendance_log.save()
            messages.success(request, "Attendance marked successfully.")
            return HttpResponseRedirect("mark_attendance")
        else:
            messages.error(request, "You are not authorized to mark attendance for this student.")
            return HttpResponseRedirect("mark_attendance")
    else:
        messages.error(request, "Scan agin please")
        return HttpResponseRedirect("mark_attendance")
        
def test(request):
    return render (request,"student_templates/mark_attendance.html")

def student_apply_leave(request):
    staff_obj = Students.objects.get(admin=request.user.id)
    leave_data=LeaveReportStudent.objects.filter(student_id=staff_obj)
    return render(request,"student_templates/student_apply_leave.html",{"leave_data":leave_data})

def student_apply_leave_save(request):
    if request.method!="POST":
        return HttpResponseRedirect("student_apply_leave")
    else:
        leave_date=request.POST.get("leave_date")
        leave_msg=request.POST.get("leave_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            leave_report=LeaveReportStudent(student_id=student_obj.id,leave_date=leave_date,leave_message=leave_msg,leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect("student_apply_leave")
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect("student_apply_leave")


def student_feedback(request):
    staff_id=Students.objects.get(admin=request.user.id)
    feedback_data=FeedBackStudent.objects.filter(student_id=staff_id)
    return render(request,"student_templates/student_feedback.html",{"feedback_data":feedback_data})

def student_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStudent(student_id=student_obj.id,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect("student_give_feedback")
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect("student_feedback")