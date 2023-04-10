from django.core.management.base import BaseCommand
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from ams_app.models import CustomUser, Staffs, Students, Subjects, Timetable, Courses, AttendanceLog, AttendanceReport
from datetime import datetime
import pytz

class Command(BaseCommand):
    help = 'Runs a function for active lectures'

    def handle(self, *args, **options):
        time=pytz.timezone("Asia/Kolkata")
        now=datetime.now(time)
        current_time=now.time()
        current_day=now.strftime("%A")
        try :
            timetable = Timetable.objects.filter(day=current_day, start_time__lte=current_time, end_time__gte=current_time).first()
            students = Students.objects.filter(course=timetable.subject.course)
            attendance_logs = AttendanceLog.objects.filter(day=datetime.now().strftime('%A'), scan_time__range=(
                    datetime.combine(datetime.today(), timetable.start_time),
                    datetime.combine(datetime.today(), timetable.end_time)
                ))
            present_students = []
            absent_students = []
            if not attendance_logs:
                absent_students = list(students)
            else:
                # Check which students are present and which are absent
                for student in Students.objects.filter(course=timetable.subject.course):
                    if attendance_logs.filter(student=student).exists():
                        present_students.append(student)
                    else:
                        absent_students.append(student)
            for student in present_students:
                    attendance_report, created = AttendanceReport.objects.get_or_create(student=student, subject=timetable.subject, attendance=attendance_logs.first())
                    attendance_report.status = 'Present'
                    attendance_report.save()
            for student in absent_students:
                    attendance_report, created = AttendanceReport.objects.get_or_create(student=student, subject=timetable.subject)
                    attendance_report.status = 'Absent'
                    attendance_report.save()
            
        except Timetable.DoesNotExist:
            pass
