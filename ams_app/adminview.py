import subprocess,pytz,json
from django.db.models import Count
from datetime import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
User = get_user_model()

from ams_app.models import CustomUser, Staffs, Students, Subjects, Timetable, Courses, AttendanceLog, AttendanceReport, LeaveReportStaff, LeaveReportStudent, FeedBackStaffs, FeedBackStudent

def admin_home(request):
    student_count1=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    total_lectures1 = AttendanceReport.objects.exclude(attendance=None).values('subject', 'created_at').distinct().annotate(count=Count('subject')).count()
    subjects_all=Subjects.objects.all()
    subject_list=[]
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
         
        return render(request,"hod_templates/home_content.html",{"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"subject_list":subject_list,'total_lectures':total_lectures1 ,"student_name_list":student_name_list,"attendance_present_list_student":attendance_present_list_student,"attendance_absent_list_student":attendance_absent_list_student})


def add_staff(request):
    return render(request,"hod_templates/add_staff.html")

def add_staff_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect("/add_staff")

def add_student(request):
    return render(request,"hod_templates/add_student.html")

def add_student_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        card_number=request.POST.get("card_number")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        address=request.POST.get("address")
        gender=request.POST.get("gender")
        try:
            user=CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=3)
            user.students.address=address
            user.students.gender=gender
            user.students.username=username
            user.students.card_number=card_number
            user.students.course_id=1
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect("/add_student")
        except:
            messages.error(request,"Failed to Add Student")
            return HttpResponseRedirect("/add_student")

def add_subject(request):
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_templates/add_subject.html",{"staffs":staffs})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)
        try:
            subject=Subjects(subject_name=subject_name,staff=staff)
            subject.course_id=1
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect("/add_subject")
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect("/add_subject")


def add_lecture(request):
    timetable=Timetable.objects.all()
    subject=Subjects.objects.all()
    return render(request,"hod_templates/add_lecture.html",{"timetable":timetable,"subjects":subject})


def add_lecture_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        start_time=request.POST.get("start_time")
        end_time=request.POST.get("end_time")
        day=request.POST.get("day")
        subject_id=request.POST.get("subject_id")
        
        try:
            timetable_update=Timetable(start_time=start_time,end_time=end_time,day=day,subject_id=subject_id)
            timetable_update.save()
            messages.success(request,"Successfully Added Lecture")
            return HttpResponseRedirect("/add_lecture")
        except:
            messages.error(request,"Failed to Add Lecture")
            return HttpResponseRedirect("/add_lecture")


def manage_staff(request):
    staffs=Staffs.objects.all()
    return render(request,"hod_templates/manage_staff.html",{"staffs":staffs})

def manage_timetable(request):
    timetable=Timetable.objects.all()
    subject=Subjects.objects.all()
    return render(request,"hod_templates/manage_timetable.html",{"timetable":timetable,"subject":subject})

def manage_student(request):
    students=Students.objects.all()
    return render(request,"hod_templates/manage_student.html",{"students":students})

def manage_subject(request):
    subjects=Subjects.objects.all()
    return render(request,"hod_templates/manage_subject.html",{"subjects":subjects})

def edit_staff(request,staff_id):
    staff=Staffs.objects.get(admin=staff_id)
    return render(request,"hod_templates/edit_staff.html",{"staff":staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect("/edit_staff/"+staff_id)
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect("/edit_staff/"+staff_id)

def edit_lecture(request,timetable_id):
    timetable=Timetable.objects.get(lecture_id=timetable_id)
    subject=Subjects.objects.all()
    return render(request,"hod_templates/edit_lecture.html",{"timetable":timetable,"subjects":subject,"id":timetable_id})

def edit_lecture_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        id=request.POST.get("lecture_id")
        start_time=request.POST.get("start_time")
        end_time=request.POST.get("end_time")
        day=request.POST.get("day")
        subject_id=request.POST.get("subject_id")
        print(id)
        try:
            timetable=Timetable.objects.get(lecture_id=id)
            timetable.start_time=start_time
            timetable.end_time=end_time
            timetable.day=day
            timetable.subject_id=subject_id
            timetable.save()
            messages.success(request,"Successfully Edited Lecture")
            return HttpResponseRedirect("/edit_lecture/"+id)
        except:
            messages.error(request,"Failed to Edit Lecture")
            return HttpResponseRedirect("/edit_lecture/"+id)

def edit_student(request,student_id):
    students=Students.objects.get(admin=student_id)
    return render(request,"hod_templates/edit_student.html",{"student":students,"id":student_id})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.POST.get("student_id")
        id_number=request.POST.get("card_number")
        email=request.POST.get("email")
        username=request.POST.get("username")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        gender=request.POST.get("gender")
        try:
            user=CustomUser.objects.get(id=student_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            student_model=Students.objects.get(admin=student_id)
            student_model.address=address
            student_model.gender=gender
            student_model.card_number=id_number
            student_model.save()
            messages.success(request,"Successfully Edited Student")
            return HttpResponseRedirect("/edit_student/"+student_id)
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect("/ledit_student/"+student_id)

def edit_subject(request,subject_id):
    subject=Subjects.objects.get(id=subject_id)
    courses=Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    return render(request,"hod_templates/edit_subject.html",{"subject":subject,"staffs":staffs,"courses":courses,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id=request.POST.get("subject_id")
        subject_name=request.POST.get("subject_name")
        staff_id=request.POST.get("staff")
        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id=staff
            subject.save()

            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect("/edit_subject/"+subject_id)
        except:
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect("/ledit_subject/"+subject_id)

def delete_staff(request, staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    try:
        staff.delete()
        messages.success(request, "Staff Deleted Successfully.")
        return HttpResponseRedirect('/manage_staff')
    except:
        messages.error(request, "Failed to Delete Staff.")
        return HttpResponseRedirect('/manage_staff')

def delete_student(request, student_id):
    student = Students.objects.get(admin=student_id)
    try:
        student.delete()
        messages.success(request, "Student Deleted Successfully.")
        return HttpResponseRedirect('/manage_student')
    except:
        messages.error(request, "Failed to Delete Student.")
        return HttpResponseRedirect('/manage_student')

def delete_subject(request, subject_id):
    subject = Subjects.objects.get(id=subject_id)
    try:
        subject.delete()
        messages.success(request, "Subject Deleted Successfully.")
        return HttpResponseRedirect('/manage_subject')
    except:
        messages.error(request, "Failed to Delete Subject.")
        return HttpResponseRedirect('/manage_subject')

def delete_lecture(request,timetable_id):
    timetable=Timetable.objects.get(lecture_id=timetable_id)
    try:
        timetable.delete()
        messages.success(request, "Lecture Deleted Successfully.")
        return HttpResponseRedirect('/manage_timetable')
    except:
        messages.error(request, "Failed to Delete Lecture")
        return HttpResponseRedirect('/manage_timetable')
    
def staff_leave_view(request):
    leaves=LeaveReportStaff.objects.all()
    return render(request,"hod_templates/staff_leave_view.html",{"leaves":leaves})

def student_leave_view(request):
    leaves=LeaveReportStudent.objects.all()
    admin=CustomUser.objects.all()
    staff=Staffs.objects.all()
    return render(request,"hod_templates/student_leave_view.html",{"leaves":leaves,"admin":admin,"staffs":staff})    

def student_approve_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect("/student_leave_view")

def student_disapprove_leave(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect("/student_leave_view")

def staff_approve_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect("/staff_leave_view")

def staff_disapprove_leave(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect("/staff_leave_view")

def staff_feedback(request):
    feedbacks=FeedBackStaffs.objects.all()
    return render(request,"hod_templates/staff_feedback.html",{"feedbacks":feedbacks})

def student_feedback(request):
    feedbacks=FeedBackStudent.objects.all()
    return render(request,"hod_templates/student_feedback.html",{"feedbacks":feedbacks})

@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def view_attendance(request):
    subjects=Subjects.objects.all()
    return render (request,"hod_templates/view_attendance.html",{"subjects":subjects})

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
    




       