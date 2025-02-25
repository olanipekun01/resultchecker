from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
# from .forms import UserSignupForm, StudentSignupForm, InstructorSignupForm
from .models import *
from django.db.models import Max, Q, F
import uuid
import random
import string
import json
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import OuterRef, Subquery, Max

from django.db.models import Sum, Min
import csv
from django.http import HttpResponse
from datetime import datetime
import os

import pandas as pd

from django.db import transaction

import fpdf
from fpdf import FPDF, HTMLMixin

from django.http import HttpResponse
from django.template.loader import render_to_string

# from weasyprint import HTML

# from io import BytesIO
# from django.template.loader import get_template
# from xhtml2pdf import pisa

from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin


from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict

from functools import reduce

from django.contrib import messages

UserModel = get_user_model()

# class UUIDEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, UUID):
#             # if the obj is uuid, we simply return the value of uuid
#             return obj.hex
#         return json.JSONEncoder.default(self, obj)

# import pdfkit
# config = pdfkit.configuration(wkhtmltopdf=r"C:\Users\AUO\Downloads\wkhtmltox-0.12.6-1.msvc2015-win64.exe")

current_academic_session = "2025/2026"
current_academic_semester = "second"


def generate_pdf(reg_course, student, session, semester, confirmReg, gpa):
    class PDF(FPDF, HTMLMixin):
        def header(self):
            # logo
            self.image("aconsa_logo.png", 10, 4, 20)
            # font
            self.set_font("helvetica", "B", 14)
            # padding
            # self.cell(0)
            # Title
            self.cell(
                179, 0, "ACHIEVERS COLLEGE OF NURSING SCIENCES, AKURE", border=False, ln=1, align="C"
            )
            # line break
            self.ln(1)

            self.set_font("helvetica", "B", 10)
            # padding
            # self.cell(75)
            # Title
            self.cell(
                170,
                7,
                "a subsidiary of",
                border=False,
                ln=1,
                align="C",
            )
            self.ln(1)

            self.set_font("helvetica", "B", 11)
            # padding
            # self.cell(75)
            # Title
            self.cell(170, 5, "ACHIEVERS UNIVERSITY, OWO", border=False, ln=1, align="C")
            self.ln(1)

            self.set_font("helvetica", "B", 10)
            # padding
            # self.cell(75)
            # Title
            self.cell(
                170,
                7,
                "www.achieversnursingcollege.edu.ng",
                border=False,
                ln=1,
                align="C",
            )
            self.ln(1)

            self.set_font("helvetica", "B", 11)
            # padding
            # self.cell(75)
            # Title
            self.cell(170, 5, "Notification of Result", border=False, ln=1, align="C")
            self.ln(1)

            
            # logo
            self.image("aconsa_logo.png", 170, 4, 23)

    pdf = PDF("P", "mm", "Letter")

    # set auto page break
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()

    pdf.ln()

    pdf.set_font("times", "B", 6)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(129, 4, f"Printed on: Monday 14th October 2024 || 12:06PM")

    pdf.set_font("times", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(
        0,
        4,
        f" {confirmReg.session.year} || {confirmReg.semester.name} SEMESTER",
        ln=True,
    )

    pdf.set_font("times", "B", 10)
    pdf.set_fill_color(6, 75, 37)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(
        180, 7, f"   :. Students' Personal Information", ln=True, fill=True, align="L"
    )

    pdf.set_font("helvetica", "BIU", 13)
    pdf.set_font("times", "B", 7)

    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 7, f"FUll NAME:")
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"{student.surname}, {student.otherNames}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 7, f"MATRIC NO / JAMB NO:")
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"{student.matricNumber} [{student.jambNumber}]", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 7, f"FACULTY / COLLEGE:")
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"{student.college}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 7, f"PROGRAMME:")
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"{student.programme}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 7, f"DEGREE:")
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"{student.degree} {student.programme}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 7, f"EMAIL / PHONE NO:")
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"{student.studentEmail} || {student.studentPhoneNumber}", ln=True)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(60, 7, f"LEVEL:")
    pdf.set_text_color(0, 0, 0)
    pdf.cell(
        0,
        7,
        f"{confirmReg.level.name}",
    )

    if student.passport:
        image_path = os.path.join(settings.MEDIA_ROOT, student.passport.name)

        if os.path.exists(image_path):

            pdf.image(image_path, 170, 58, 23)

    pdf.ln()

    # pdf.cell(100, 10, 'Title', border=0, fill=True)
    # pdf.cell(15, 10, 'Unit', border=0, fill=True)

    # pdf.set_font('Arial', 'B', 8)
    # pdf.set_fill_color(0, 0, 0)
    # pdf.set_text_color(255, 255, 255)
    # pdf.cell(25, 8, 'Code', border=1, fill=True)
    # pdf.cell(100, 8, 'Title', border=1, fill=True)
    # pdf.cell(15, 8, 'Unit', border=1, fill=True)
    # pdf.cell(15, 8, 'Status', border=1, fill=True)
    # pdf.cell(30, 8, 'Signature', border=1, fill=True)
    # pdf.ln()

    # Add table rows with padding and borders
    pdf.set_font("Arial", "B", 6)
    pdf.set_text_color(0, 0, 0)
    unit = 0
    pdf.cell(25, 4, f"Code", border=1)
    pdf.cell(100, 4, f"Title", border=1)
    pdf.cell(15, 4, f"Unit", border=1)
    pdf.cell(15, 4, f"Score", border=1)
    pdf.cell(15, 4, f"Grade", border=1)
    pdf.ln()
    for co in reg_course:
        pdf.cell(25, 4, f"{co.registration.course.courseCode}", border=1)
        pdf.cell(100, 4, f"{co.registration.course.title}", border=1)
        pdf.cell(15, 4, f"{co.registration.course.unit}", border=1)
        pdf.cell(15, 4, f"{co.grade}", border=1)
        pdf.cell(15, 4, f"{co.grade_type}", border=1)
        
        pdf.ln()
        unit += co.registration.course.unit

    pdf.set_font("Arial", "B", 6)
    pdf.cell(25, 4, f"", border=1)
    pdf.cell(100, 4, f"Total Registered Units", border=1)
    pdf.cell(15, 4, f"{unit}", border=1)
    pdf.cell(15, 4, f"GPA", border=1)
    pdf.cell(15, 4, f"{gpa}", border=1)
    pdf.ln()

    pdf.set_font("helvetica", "BIU", 16)
    pdf.set_font("times", "", 9)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"Key: C=Core, E=Elective, R=Required", ln=True)

    pdf.ln(4)

    pdf.set_font("helvetica", "BIU", 16)
    pdf.set_font("times", "", 7)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(145, 7, f"Signature of Student: _____________________________________")
    pdf.cell(0, 7, f"Date: __________________________", ln=True)

    pdf.set_font("times", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(180, 7, f"FOR OFFICIAL USE ONLY", align="C", ln=True)

    pdf.set_font("times", "B", 6)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(
        180,
        2,
        f"I certify that the above named student has submitted four(4) copies of his/her first semester course registration form and he/she is qualified to register the above listed courses",
        align="C",
        ln=True,
    )

    pdf.ln(6)

    pdf.set_font("helvetica", "BIU", 16)
    pdf.set_font("times", "", 7)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(145, 7, f"Signature of Academic Advisor: ____________________________")
    pdf.cell(0, 7, f"Date: __________________________", ln=True)
    pdf.ln(6)

    pdf.set_font("helvetica", "BIU", 16)
    pdf.set_font("times", "", 7)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(145, 7, f"Signature of H.O.D.: _____________________________________")
    pdf.cell(0, 7, f"Date: __________________________", ln=True)
    pdf.ln(6)

    pdf.set_font("helvetica", "BIU", 16)
    pdf.set_font("times", "", 7)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(145, 7, f"Signature of DEAN: _____________________________________")
    pdf.cell(0, 7, f"Date: __________________________", ln=True)

    pdf.ln(3)

    pdf.set_font("times", "B", 6)
    pdf.set_text_color(255, 0, 0)
    pdf.cell(
        180,
        2,
        f"Note:This form should be printed and returned to the Examination Officer at least Four weeks before the commencement of the examinations.",
        align="C",
        ln=True,
    )
    pdf.cell(
        180,
        2,
        f"No Candidate shall be allowed to write any \nexamination in any course unless he/she has satisfied appropriate registration & finanacial regulations.",
        align="C",
    )

    return pdf
    # for i in range (1, 41):
    #     pdf.cell(0, 10, f'This is line {i} :D', ln=True)
    # pdf.output('fpdfdemo.pdf', 'F')




def set_current_session(session_id):
    # Set all sessions to not current
    Session.objects.all().update(is_current=False)
    # Set the specified session as current
    session = Session.objects.get(id=session_id)
    session.is_current = True
    session.save()


# Helper functions for role checks
def is_student(user):
    # print("User", User.role)
    return user.user_type == "student"
    # return True


def is_instructor(user):
    return user.user_type == "instructor"

def is_advisor(user):
    return user.user_type == "leveladvisor"



def generate_password(length=8):
    """Generate a random password."""
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for i in range(length))


# def is_student_registered_for_semester(student, semester, session):
#     """
#     Check if a student is registered for a specific semester in a session.
#     :param student: The student instance
#     :param semester: The semester to check (e.g., 'First', 'Second')
#     :param session: The session instance (e.g., '2023/2024')
#     :return: True if registered, False otherwise
#     """
#     return Registration.objects.filter(
#         student=student, semester=semester, session=session
#     ).exists()

# Create your views here.


from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
import json


@login_required
@user_passes_test(is_student, login_url="/404")
def Dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        student = get_object_or_404(Student, user=user)

        level = get_object_or_404(Level, name=student.currentLevel)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()   
        
        if request.method == "POST":
            template = request.POST["template"]

        return render(request, "user/dashboard.html", {'student': student})

@login_required
@user_passes_test(is_student, login_url="/404")
def Courses(request):
    if request.user.is_authenticated:
        user = request.user
        student = get_object_or_404(Student, user=user)

        level = get_object_or_404(Level, name=student.currentLevel)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()   
        
        if request.method == "POST":
            courses = request.POST.getlist(
                "courses"
            )  
            # sess = request.POST["sess"]
            # semes = request.POST["semes"]
            totalUnit = request.POST["totalUnit"]
             # Filter registrations for the student, session, and semester
            registrations = Registration.objects.filter(
                student=student,
                session=current_session_model,
                semester=current_semester_model
            )

            # Aggregate the total units by summing the 'unit' field of related courses
            total_units = registrations.aggregate(total_units=Sum('course__unit'))['total_units']

            # Handle the case where no registrations exist
            total_units = total_units or 0

            if total_units <= 24:
                for id in courses:
                    
                    course = (get_object_or_404(Course, id=id),)
                    print("course name", course)
                    semester = current_semester_model
                    

                    course_exist = Registration.objects.create(
                        student=student,
                        course=get_object_or_404(Course, id=id),
                        session=current_session_model,
                        semester=current_semester_model,
                    )
                    course_exist.save()

                # Default to 0 if no units are found

                print(f"Total units registered: {total_units}")

                confirm_reg, created = confirmRegister.objects.get_or_create(
                    student=student,
                    session=current_session_model,
                    semester=current_semester_model,
                    level=get_object_or_404(Level, name=student.currentLevel),
                )

                if not created:
                    # Update the total units and registration date if the instance already exists
                    confirm_reg.totalUnits = total_units
                    confirm_reg.registration_date = now().date()
                    confirm_reg.save()
                else:
                    # If a new instance was created, set the totalUnits and save
                    confirm_reg.totalUnits = total_units
                    confirm_reg.save()
                messages.info(request, "Course added")
                return redirect("/courses/")
            messages.error(request, "Exceeded maximum units")
            return redirect('/courses/')
        
        level = get_object_or_404(Level, name=student.currentLevel)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()
        try:
            current_semester_model = Semester.objects.get(is_current=True)
        except ObjectDoesNotExist:
            # raise ValueError("No current semester is set. Please set one as current.")
            messages.error(request, "No current semester is set. Please set one as current.")
            return redirect('/courses/')

        # Get the current session
        try:
            current_session_model = Session.objects.get(is_current=True)
        except ObjectDoesNotExist:
            messages.error(request, "No current semester is set. Please set one as current.")
            return redirect('/courses/')
        
        courses = Course.objects.filter(
            level=level, 
            programme=student.programme, 
            semester=current_semester_model,
        )

        

        registered_courses = Registration.objects.filter(
            student=student, 
            semester=current_semester_model,
            session=current_session_model  # Ensure this is the current academic session
        ).values_list('course', flat=True)

        courses = courses.exclude(id__in=registered_courses)

       
        # Step 1: Retrieve the current session and semester
        current_session = Session.objects.filter(is_current=True).first()
        current_semester = Semester.objects.filter(is_current=True).first()

        if not current_session or not current_semester:
            messages.error(request, "No current semester is set. Please set one as current.")
            return redirect('/courses/')

        # registrations = Registration.objects.filter(student=student)

        # # Step 2: Filter registrations not in the current session AND current semester
        # registrations = registrations.filter(
        #     ~Q(session=current_session) & Q(semester=current_semester)
        # )

        # # Debugging: Print the filtered registrations
        # print("Registrations not in current session and semester:", registrations)

        # annotated_courses = registrations.annotate(latest_registration_date=Max('registration_date'))
        # print('annotated_courses', annotated_courses)

        # # Step 3: Filter only the latest registrations
        # carryover_courses_unique = annotated_courses.filter(
        #     registration_date=F('latest_registration_date')
        # )

        latest_attempts = Result.objects.filter(
            registration__student=student  # Filter by the specific student
        ).values('registration_id').annotate(
            highest_attempt=Max('attempt_number')
        )

        # print('latests', latest_attempts)

        # Step 2: Filter results with the highest attempt where the grade remark is not 'passed'
        # failed_results = Result.objects.filter(
        #     Q(attempt_number__in=[attempt['highest_attempt'] for attempt in latest_attempts]),
        #     registration__student=student,  # Ensure we only consider the same student
        #     grade_remark__in=['failed', 'pending']
        # )

        # failed_results = Result.objects.filter(
        #     Q(
        #         *[
        #             Q(registration_id=attempt['registration_id'], attempt_number=attempt['highest_attempt'])
        #             for attempt in latest_attempts
        #         ]
        #     ),
        #     grade_remark__in=['failed', 'pending']  # Filter for failed or pending results
        # )

        # print('results', failed_results)

        # Step 1: Verify latest attempts
        latest_attempts = Result.objects.filter(
            registration__student=student
        ).values('registration_id').annotate(
            highest_attempt=Max('attempt_number')
        )
        # print("Latest Attempts:", list(latest_attempts))

        # Step 2: Construct the query for failed results
        conditions = [
            Q(registration_id=attempt['registration_id'], attempt_number=attempt['highest_attempt'])
            for attempt in latest_attempts
        ]

        if conditions:
            failed_results = Result.objects.filter(
                reduce(lambda x, y: x | y, conditions),  # Combine conditions with OR
                grade_remark__in=['failed', 'pending']
            )
            # print("Failed Results:", list(failed_results))
        else:
            failed_results = Result.objects.none()  # No conditions mean no results

        # Final debug print
        # print("Final Failed Results:", failed_results)


        

        # Step 1: Filter all registrations for the student
        registrations = Registration.objects.filter(student=student)

        # Step 2: Identify courses registered in the current session
        courses_in_current_session = registrations.filter(
            session=current_session
        ).values_list('course_id', flat=True)

        # Step 3: Filter registrations not in the current session, but in the current semester,
        # and exclude any course that has been registered in the current session
        registrations = registrations.filter(
            ~Q(course_id__in=courses_in_current_session),  # Exclude courses registered in current session
            semester=current_semester  # Include only courses in current semester
        )

        registrations = registrations.filter(
            id__in=failed_results.values_list('registration_id', flat=True),
            student=student  # Additional filter for the same student
        )

        # Debugging: Print the filtered registrations
        # print("Registrations not in current session but in current semester:", registrations)

        # Step 4: Annotate to get the latest registration date for each course
        annotated_courses = registrations.annotate(latest_registration_date=Max('registration_date'))
        # print('Annotated courses:', annotated_courses)

        # Step 5: Filter only the latest registrations
        carryover_courses_unique = annotated_courses.filter(
            registration_date=F('latest_registration_date')
        )

        # Debugging: Print final carryover courses
        # print("Final Carryover Courses:", carryover_courses_unique)


        # print('latest_registrations', carryover_courses_unique)


        registrations = Registration.objects.filter(student=student).select_related('session')
        
        enrollment = Enrollment.objects.filter(student=student).order_by('enrolled_date').first()

        enrollment_year = int(enrollment.session.year.split('/')[0])

        # Calculate level for each session
        sessions_and_levels = []
        for registration in registrations:
            session_year = int(registration.session.year.split('/')[0])
            # Calculate the difference in years
            years_since_enrollment = session_year - enrollment_year
            # Calculate the level, assuming the student starts at Level 100 and progresses yearly
            current_level = 100 + (years_since_enrollment * 100)
            
            sessions_and_levels.append({
                'session': registration.session.year,
                'level': current_level,
                'registration': registration,  # Add any course details if necessary
            })
        
        cObjects = Course.objects.all().filter(department=student.department)
        course_levels = []
        for x in cObjects:
            course_levels.append(x.level.name)
        course_levels.sort(key=str)
        course_levels = list(set(course_levels))
        # print('course_levels', course_levels)

        confirmReg = confirmRegister.objects.filter(student=student)

        unique_sessions = sorted({entry['session'] for entry in sessions_and_levels})
        
        unique_levels = sorted({entry['level'] for entry in sessions_and_levels})

        

        # courses = Course.objects.all()

        duration = 0
        if len(unique_levels) == len(unique_sessions):
            duration = len(unique_levels)

        
        return render(
            request,
            "user/courses.html",
            {
                "courses": courses,
                "student": student,
                "sess": current_session_model,
                "semes": current_semester_model,
                "carryover": carryover_courses_unique,
                'sessions_and_levels': sessions_and_levels,
                'unique_sessions': unique_sessions, 
                'unique_levels': unique_levels, 
                'duration':duration,
                'confirmReg': confirmReg,
            },
        )

    # return render(request, "user/courses.html", {"student": 'student'})

@login_required
@user_passes_test(is_student, login_url="/404")
def CourseDelete(request, id):
    if request.user.is_authenticated:
        user = request.user
        student = get_object_or_404(Student, user=user)

        level = get_object_or_404(Level, name=student.currentLevel)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()

        try:
            reg = Registration.objects.filter(id=id).first()
            if reg.session == current_session_model and reg.semester == current_semester_model and reg.instructor_remark == 'rejected':
                messages.info(request, f'Deleted {reg.course.title}!!')
                
                reg.delete()

                registrations = Registration.objects.filter(
                    student=student,
                    session=current_session_model,
                    semester=current_semester_model
                )

                # Aggregate the total units by summing the 'unit' field of related courses
                total_units = registrations.aggregate(total_units=Sum('course__unit'))['total_units']

                # Handle the case where no registrations exist
                total_units = total_units or 0  # Default to 0 if no units are found

                print(f"Total units registered: {total_units}")
                
                confirm_reg, created = confirmRegister.objects.get_or_create(
                    student=student,
                    session=current_session_model,
                    semester=current_semester_model,
                    level=get_object_or_404(Level, name=student.currentLevel),
                )

                if not created:
                    # Update the total units and registration date if the instance already exists
                    confirm_reg.totalUnits = total_units
                    confirm_reg.registration_date = now().date()
                    confirm_reg.save()
                else:
                    # If a new instance was created, set the totalUnits and save
                    confirm_reg.totalUnits = total_units
                    confirm_reg.save()
                
                return redirect("/courses")
            else:
                messages.info(request, f'Request not allowed')
                return redirect("/courses/")
                 
        except:
            messages.info(request, f'Registered Course not available')
            return redirect("/courses/")
        
@login_required
@user_passes_test(is_student, login_url="/404")
def ResultFilter(request):
    if request.user.is_authenticated:
        user = request.user
        student = get_object_or_404(Student, user=user)

        level = get_object_or_404(Level, name=student.currentLevel)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first() 

        # Get the earliest session the student was enrolled in
        earliest_session = student.entrySession.order_by('id').first()

        print('earliest0', earliest_session)        
        # Get all sessions from the earliest session onward
        if earliest_session:
            sessions_from_earliest = Session.objects.filter(id__gte=earliest_session.id)
            print('session from earliest0', sessions_from_earliest)
        else:
            sessions_from_earliest = Session.objects.none()  # No sessions available

        # Print sessions for debugging
        
        if request.method == "POST":
            sess = request.POST["session-select"]
            semes = request.POST["semester-select"]

            session = get_object_or_404(Session, year=sess)
            semester = get_object_or_404(Semester, name=semes)

            registration = Result.objects.filter(registration__student=student, registration__session=session, registration__semester=semester)

            if registration.exists():
                # Get all attempts sorted by attempt date (latest first)
                attempts = registration.order_by('result_date')
                latest_attempt = attempts.first()

                

               

               

                # latest_attempt = Result.objects.filter(
                #     registration__student=student, registration__session=session, registration__semester=semester
                # ).values('registration_id').annotate(
                #     highest_attempt=Max('attempt_number')
                # )

                latest_attempt = Result.objects.filter(
                    registration_id=OuterRef('registration_id')
                ).values('registration_id').annotate(
                    highest_attempt=Max('attempt_number')
                ).values('highest_attempt')

                latest_results = Result.objects.filter(
                    attempt_number=Subquery(latest_attempt),
                    registration__student=student  # Ensure it is for the specific student
                )

                


                # Use list comprehension to keep the latest result for each course
                
                # for registration in attempts:
                #     if registration.registration.course.id not in processed_courses:
                #         processed_courses.append(registration)
                

                # latest_results = (
                #     registration.values('registration__course_id')  # Group by course
                #     .annotate(latest_attempt_date=Max('result_date'))  # Find the latest result_date
                # )

                # # Filter the results to include only the latest attempts
                # latest_attempts = Result.objects.filter(
                #     registration__course_id__in=[result['registration__course_id'] for result in latest_results],
                #     result_date__in=[result['latest_attempt_date'] for result in latest_results]
                # ).order_by('registration__course__courseCode')  # Optional ordering

                

                # Calculate total credit units
                total_credit_units = sum(course.registration.course.unit for course in attempts)

                # Calculate total points
                total_points = sum(course.total_point for course in attempts)

                # Calculate GPA
                gpa = total_points / total_credit_units if total_credit_units > 0 else 0

                

                return render(request, "user/resultview.html", {
                    "status": "success",
                    "latest_attempt": latest_attempt,
                    "all_attempts": attempts,
                    "results": latest_results,
                    "total_credit_units": total_credit_units,
                    "total_points": total_points,
                    "gpa": round(gpa, 2),
                    "total_course": len(attempts),
                    "session": session.year,
                    "semester": semester.name,
                })
            else:
                if not Result.objects.filter(registration__session=session, registration__semester=semester).exists():
                    messages.error(request, "Results have not been uploaded yet for this session and semester.")
                    return redirect("/result/filter")
                else:
                    messages.error(request, "No results found for this student in the selected session and semester.")
                    return redirect("/result/filter")
                    

        return render(request, "user/resultfilter.html", {'sessions': sessions_from_earliest})

@login_required
@user_passes_test(is_student, login_url="/404")
def ResultView(request):
    if request.user.is_authenticated:
        user = request.user
        student = get_object_or_404(Student, user=user)

        level = get_object_or_404(Level, name=student.currentLevel)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()   
        
        if request.method == "POST":
            template = request.POST["template"]

        return render(request, "user/resultview.html")
    
@login_required
@user_passes_test(is_student, login_url="/404")
def ResultView(request):
    if request.user.is_authenticated:
        user = request.user
        student = get_object_or_404(Student, user=user)

        level = get_object_or_404(Level, name=student.currentLevel)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()

        if request.method == 'POST':
            sess = request.POST['sess']
            semes = request.POST['semes']
            session = get_object_or_404(Session, year=sess)
            semester = get_object_or_404(Semester, name=semes)

            registration = Result.objects.filter(registration__student=student, registration__session=session, registration__semester=semester)

            if registration.exists():
                # Get all attempts sorted by attempt date (latest first)
                print('reg i', registration)
                attempts = registration.order_by('result_date')
                print('reg ii', attempts)
                latest_attempt = attempts.first()


                # Calculate total credit units
                total_credit_units = sum(course.registration.course.unit for course in attempts)

                # Calculate total points
                total_points = sum(course.total_point for course in attempts)

                # Calculate GPA
                gpa = total_points / total_credit_units if total_credit_units > 0 else 0

                

                reg_courses = Registration.objects.filter(
                    student=student,
                    semester=get_object_or_404(Semester, name=semes),
                    session=get_object_or_404(Session, year=sess),
                )

                confirmReg = confirmRegister.objects.filter(
                    student=student,
                    semester=get_object_or_404(Semester, name=semes),
                    session=get_object_or_404(Session, year=sess),
                ).first()

                gen = generate_pdf(attempts, student, sess, semes, confirmReg, gpa)

                gen.output("fpdfdemo.pdf", "F")

                response = HttpResponse(
                    gen.output(dest="S").encode("latin1"), content_type="application/pdf"
                )
                # response['Content-Disposition'] = 'attachment; filename="fpdfdemo.pdf"'

                response["Content-Disposition"] = 'inline; filename="preview.pdf"'
                return response


        return render(request, "user/resultfilter.html")
    

@login_required
@user_passes_test(is_student, login_url="/404")
def Contact(request):
    if request.user.is_authenticated:
        user = request.user
        student = get_object_or_404(Student, user=user)

        level = get_object_or_404(Level, name=student.currentLevel)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()   
        
        if request.method == "POST":
            template = request.POST["template"]

        return render(request, "contact.html")


@login_required
@user_passes_test(is_student, login_url="/404")
def changePassword(request):
    if request.method == "POST":
        old_password = request.POST["oldpassword"]
        new_password = request.POST["newpassword"]
        confirm_password = request.POST["newpassword"]

        if new_password != confirm_password:
            return render(
                request, "user/changepassword.html", {"error": "Use same password"}
            )
        
        if len(new_password) < 8:
            return render(
                request, "user/changepassword.html", {"error": "Password too short, > than 8 characters!"}
            )

        user = request.user

        if user.check_password(old_password):
            user.set_password(new_password)
            user = auth.authenticate(username=user.username, password=new_password)
            auth.login(request, user)
            return render(
                request,
                "user/changepassword.html",
                {"success": "Password Change Successful!"},
            )
        else:
            error_message = "Incorrect old password."
            return render(request, "user/changepassword.html", {"error": error_message})

    return render(request, "user/changepassword.html")


@login_required
@user_passes_test(is_instructor, login_url="/404")
def adminDashboard(request):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        countProgrammes = len(
            Programme.objects.filter(department=instructor.department)
        )
        countCourses = len(Course.objects.filter(department=instructor.department))

    return render(
        request,
        "admin/admin_dashboard.html",
        {
            "countProgrammes": countProgrammes,
            "countCourses": countCourses,
            "department": instructor.department,
        },
    )

@login_required
@user_passes_test(is_instructor, login_url="/404")
def adminProgrammeManagement(request):
    if request.user.is_authenticated:

        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        # programmes = Programme.objects.filter(department=instructor.department)
        programmes = Programme.objects.all()
        # countCourses = len(Course.objects.filter(department=instructor.department))
        if request.method == "POST":
            programme_name = request.POST["programme_name"]
            programme_duration = request.POST["programme_duration"]
            programme_degree = request.POST["programme_degree"]
            programme_dept = request.POST["programme_dept"]

            if (
                programme_name != ""
                and programme_duration != ""
                and programme_degree != ""
            ):
                try:
                    if Programme.objects.all().filter(name=programme_name).exists():
                        messages.info(request, "Programme already exist!")
                        return redirect("/instructor/programmes")

                    programmeObjects = Programme.objects.create(
                        name=programme_name,
                        department=get_object_or_404(Department, id=programme_dept),
                        duration=programme_duration,
                        degree=programme_degree,
                    )
                    programmeObjects.save()
                    messages.info(request, "Programme Added!")
                    return redirect("/instructor/programmes")
                except:
                    messages.info(request, f"Programme not available")
                    return redirect("/instructor/programmes")
            else:
                messages.info(request, f"Fields cannot be empty")
                return redirect("/instructor/programmes")

        return render(
            request,
            "admin/admin_program_management.html",
            {
                "programmes": programmes,
                "department": instructor.department,
                "allDepts": Department.objects.all()
            },
        )

@login_required
@user_passes_test(is_instructor, login_url="/404")
def adminProgrammeDepartmentManagement(request, dept):
    if request.user.is_authenticated:

        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        programmes = Programme.objects.all()

        prog = get_object_or_404(Programme, id=dept)

        levels = Level.objects.all()

        return render(
        request,
        "admin/admin_program_dept_management.html",
        {
            "programmes": programmes,
            "dept": dept,
            "levels": levels,
            "departs": prog.name
        },
    )

@login_required
@user_passes_test(is_instructor, login_url="/404")
def adminProgrammeDepartmentLevelManagement(request, dept, level):
    if request.user.is_authenticated:

        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        programmes = Programme.objects.all()


        students = Student.objects.all().filter(
            programme=get_object_or_404(Programme, id=dept),
            currentLevel=level,
        )

        

        prog = Programme.objects.all().filter(id=dept).first()

    
        return render(
        request,
        "admin/level_student_list.html",
        {
            "programmes": programmes,
            "departs": prog.name,
            "studentlist": students,
            "level": level,

        },
    )

@login_required
@user_passes_test(is_instructor, login_url="/404")
def UpdateProgramme(request):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        if request.method == "POST":
            p_id = request.POST["programme_id"]
            p_name = request.POST["programme_name"].strip()
            p_duration = request.POST["programme_duration"].strip()
            p_degree = request.POST["programme_degree"].strip()
            p_dept= request.POST["programme_dept"].strip()

            if p_name != "" and p_duration != "" and p_degree != "":
                try:
                    programmes = Programme.objects.filter(
                        id=p_id
                    )[0]
                    programmes.name = p_name
                    programmes.degree = p_degree
                    programmes.duration = p_duration
                    programmes.department = get_object_or_404(Department, id=p_dept)
                    programmes.save()
                    messages.info(request, f"Programme Updated")
                    return redirect("/instructor/programmes")
                except:
                    messages.info(request, f"Programme not available")
                    return redirect("/instructor/programmes")
            messages.info(request, f"Fields cannot be empty")
            return redirect("/instructor/programmes")
        return redirect("/instructor/programmes")


@login_required
@user_passes_test(is_instructor, login_url="/404")
def deleteProgramme(request, id):

    try:
        program = Programme.objects.filter(id=id)[0]
        print("1", program.name)
        if Programme.objects.all().filter(id=id).exists():
            messages.info(request, f"{program.name} deleted successfully")
            program = Programme.objects.filter(id=id).delete()

            return redirect("/instructor/programmes")
        messages.info(request, f"Programme not available")
        return redirect("/instructor/programmes")
    except:
        messages.info(request, f"Programme not available")
        return redirect("/instructor/programmes")
    
@login_required
@user_passes_test(is_instructor, login_url="/404")
def adminDepartmentManagement(request):
    if request.user.is_authenticated:

        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        # programmes = Programme.objects.filter(department=instructor.department)
        departments = Department.objects.all()
        # countCourses = len(Course.objects.filter(department=instructor.department))
        if request.method == "POST":
            dept_name = request.POST["department_name"]

            if (
                dept_name != ""
            ):
                try:
                    if Department.objects.all().filter(name=dept_name).exists():
                        messages.info(request, "Department already exist!")
                        return redirect("/instructor/departments")

                    deptObjects = Department.objects.create(
                        name=dept_name,
                        college=get_object_or_404(College, id="e3aba966-49f1-40b1-a07a-7a79e32aac5d"),
                    )
                    deptObjects.save()
                    messages.info(request, "Department Added!")
                    return redirect("/instructor/departments")
                except:
                    messages.info(request, f"Something went wrong")
                    return redirect("/instructor/departments")
            else:
                messages.info(request, f"Fields cannot be empty")
                return redirect("/instructor/departments")

        return render(
            request,
            "admin/admin_department_management.html",
            {
                "departments": departments,
            },
        )
    
@login_required
@user_passes_test(is_instructor, login_url="/404")
def UpdateDepartment(request):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        if request.method == "POST":
            dept_id = request.POST["department_id"]
            dept_name = request.POST["department_name"].strip()

            if dept_name != "":
                try:
                    department = Department.objects.filter(
                        id=dept_id
                    )[0]
                    department.name = dept_name
                    department.save()
                    messages.info(request, f"Department Updated")
                    return redirect("/instructor/departments")
                except:
                    messages.info(request, f"Department not available")
                    return redirect("/instructor/departments")
            messages.info(request, f"Fields cannot be empty")
            return redirect("/instructor/departments")
        return redirect("/instructor/departments")


@login_required
@user_passes_test(is_instructor, login_url="/404")
def deleteDepartment(request, id):

    try:
        department = Department.objects.filter(id=id)[0]
        print("1", department.name)
        if Department.objects.all().filter(id=id).exists():
            messages.info(request, f"{department.name} deleted successfully")
            department = Department.objects.filter(id=id).delete()

            return redirect("/instructor/departments")
        messages.info(request, f"Department not available")
        return redirect("/instructor/departments")
    except:
        messages.info(request, f"Department not available")
        return redirect("/instructor/departments")

@login_required
@user_passes_test(is_instructor, login_url="/404")
def adminLevelDepartmentManagement(request, dept):
    if request.user.is_authenticated:

        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        programmes = Programme.objects.all()

        department = get_object_or_404(Department, id=dept)

        levels = Level.objects.all()

        return render(
        request,
        "admin/admin_department_level.html",
        {
            "programmes": programmes,
            "dept": dept,
            "levels": levels,
            "departs": department.name
        },
    )

@login_required
@user_passes_test(is_instructor, login_url="/404")
def adminStudentListDepartment(request, dept, level):
    if request.user.is_authenticated:

        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        programmes = Programme.objects.all()


        students = Student.objects.all().filter(
            department=get_object_or_404(Department, id=dept),
            currentLevel=level,
        )

        

        dept = Department.objects.all().filter(id=dept).first()

    
        return render(
        request,
        "admin/dept_level_student_list.html",
        {
            "programmes": programmes,
            "departs": dept.name,
            "studentlist": students,
            "level": level,

        },
    )

@login_required
@user_passes_test(is_instructor, login_url="/404")
def CourseDept(request):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)

        depts = Department.objects.all()
        return render(request, 'admin/course_dept.html', {'depts': depts, "department": "instructor"})

@login_required
@user_passes_test(is_instructor, login_url="/404")
def adminCourseManagement(request, dept):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        # courses = Course.objects.all().filter(department=instructor.department)
        courses = [
        {
            "id":  str(course.id),
            "title": course.title,
            "code": course.courseCode,
            "unit": course.unit,
            "status": course.status,
            "level": course.level.name,
            "semester": course.semester.name,
            "category": course.category,
            "programmes": [str(prog_id) for prog_id in course.programme.values_list("id", flat=True)]  # Convert each programme ID to string
        }
        for course in Course.objects.all().filter(department=get_object_or_404(Department, id=dept))
        ]
        # print('see courses', courses[0].title)
        cObjects = Course.objects.all().filter(department=get_object_or_404(Department, id=dept))
        course_levels = []
        for x in cObjects:
            course_levels.append(x.level.name)
        course_levels.sort(key=str)
        course_levels = list(set(course_levels))
        print('course', course_levels)
        programmes = Programme.objects.all().filter(department=get_object_or_404(Department, id=dept))
        # selected_programmes = courseObjects.programmes.all()
        if request.method == "POST":
            course_title = request.POST["course_title"].strip()
            course_code = request.POST["course_code"].strip()
            course_unit = request.POST["course_unit"].strip()
            course_status = request.POST["course_status"].strip()
            course_cat = request.POST["courseCat"]
            # program = request.POST['programme']
            level = request.POST["level"]
            semester = request.POST["semester"]

            if (
                course_title == ""
                and course_code == ""
                and course_unit == ""
                and course_status == ""
            ):
                messages.info(request, f"Fields cannot be empty")
                return redirect(f"/instructor/courses/{dept}")

            if Course.objects.all().filter(courseCode=course_code).exists():
                messages.info(request, "Course already exist!")
                return redirect(f"/instructor/courses/{dept}")

            courseObjects = Course.objects.create(
                title=course_title,
                courseCode=course_code,
                department=instructor.department,
                unit=course_unit,
                category=course_cat,
                status=course_status,
                level=get_object_or_404(Level, name=level),
                semester=get_object_or_404(Semester, name=semester),
            )

            courseObjects.save()
            programmes_ids = request.POST.getlist('programmes')  # Assuming departments are selected in a form
            
            programmes = Programme.objects.filter(pk__in=programmes_ids)
            # Add all retrieved Programme instances to the courseObjects' programmes field
            courseObjects.programme.add(*programmes)
            messages.info(request, 'Course Added!')
            return redirect(f'/instructor/courses/{dept}')

    return render(request, 'admin/course_management.html', {'courses': courses, 'courseLevels': course_levels, "programme": programmes, "department": instructor.department, "deptid": dept})

@login_required
@user_passes_test(is_instructor, login_url="/404")
def updateCourse(request, dept):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        if request.method == "POST":
            course_id = request.POST["course_id"]
            course_title = request.POST["course_title"].strip()
            course_code = request.POST["course_code"].strip()
            course_unit = request.POST["course_unit"].strip()
            course_status = request.POST["course_status"].strip()
            course_cat = request.POST["courseCat"]
            level = request.POST["level"]
            semester = request.POST["semester"]
            # program = request.POST['programmes']

            if ( course_title != "" and course_code != "" and course_unit != "" and course_status != ""):
                try:
                    courseObjects = Course.objects.filter(
                        department=get_object_or_404(Department, id=dept), id=course_id
                    )[0]
                    courseObjects.title = course_title
                    courseObjects.courseCode = course_code
                    courseObjects.unit = course_unit
                    courseObjects.status = course_status
                    courseObjects.category = course_cat
                    courseObjects.level = get_object_or_404(Level, name=level)
                    courseObjects.semester = get_object_or_404(Semester, name=semester)
                    # courseObjects.programme = get_object_or_404(Programme, id=program)
                    courseObjects.save()
                    programmes_ids = request.POST.getlist('programmes')  # Assuming departments are selected in a form
                    
                    programmes = Programme.objects.filter(pk__in=programmes_ids)

                    # Add all retrieved Programme instances to the courseObjects' programmes field
                    courseObjects.programme.set(programmes)
                    messages.info(request, f'Course Updated')
                    return redirect(f"/instructor/courses/{dept}")
                except:
                    messages.info(request, f'Course not available')
                    return redirect(f"/instructor/courses/{dept}")
            messages.info(request, f'Fields cannot be empty')
            return redirect(f"/instructor/courses/{dept}")
        return redirect(f"/instructor/courses/{dept}")


@login_required
@user_passes_test(is_instructor, login_url='/404')
def deleteCourse(request, dept, id):

    try:
        courseObjects = Course.objects.filter(
            department=get_object_or_404(Department, id=dept), id=id
        )[0]
        print("1", courseObjects.title)
        if Course.objects.all().filter(id=id).exists():
            messages.info(request, f'{courseObjects.title} deleted successfully')
            course= Course.objects.filter(id=id).delete()
            
            return redirect(f"/instructor/courses/{dept}")
        messages.info(request, f'Course not available')
        return redirect(f"/instructor/courses/{dept}")
    except:
        messages.info(request, f'Course not available')
        return redirect(f"/instructor/courses/{dept}")
    

@login_required
@user_passes_test(is_instructor, login_url='/404')
def eachCourse(request, id):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        session = Session.objects.all()
        course = Course.objects.all().filter(department=instructor.department, id=id).first()
        if request.method == 'POST':
            sess = request.POST['session']
            semes = request.POST['semester']
            if sess != "" and semes != "":
                sess = get_object_or_404(Session, year=sess)
                semes = get_object_or_404(Semester, name=semes)
                
                register = Registration.objects.all().filter(session=sess, semester=semes, course=get_object_or_404(Course, id=id))
                print('register', register)

                return render(request, 'admin/each_course.html', {'course': course, "department": instructor.department, 'session': session, 'registered_student': register,
                                                                  'down_sess':sess, 'down_semes':semes, 'course_id':id})
            
            messages.info(request, f'Information not available')
            redirect(f"/instructor/courses/each/{id}/")
    return render(request, 'admin/each_course.html', {'course': course, "department": instructor.department, 'session': session})

@login_required
@user_passes_test(is_instructor, login_url='/404')
def DownloadStudentCourse(request):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        
        if request.method == 'POST':
            id = request.POST['course_id']
            sess = request.POST['session_year']
            semes = request.POST['semester_name']

            course = get_object_or_404(Course, id=id)
            sess = get_object_or_404(Session, year=sess)
            semes = get_object_or_404(Semester, name=semes)
            registrations = Registration.objects.filter(course=course, session=sess, semester=semes)

            # Create HTTP response with CSV content type
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="course_registration_{course.id}_{sess.year}.csv"'

            # Create CSV writer
            writer = csv.writer(response)

            # Write header row
            writer.writerow(['Registration Id', 'Grade', 'Student Id', 'Matric No', 'Student Name', 'Course id', 'Course Code', 'Course Title', 'Session', 'Semester', 'Level', 'Total Units'])


            # Write data rows
            for registration in registrations:
                student = registration.student
                course = registration.course
                session = registration.session
                semester = registration.semester
                writer.writerow([
                    registration.id,
                    "",  # Leave grade blank for result upload
                    student.user.id,
                    student.matricNumber,
                    f"{student.otherNames} {student.surname}",
                    course.id,
                    course.courseCode,
                    course.title,
                    session.year,
                    semester.name,
                    course.level.name,
                    course.unit,
                    
                ])

            return response

@login_required
@user_passes_test(is_instructor, login_url='/404')
def upload_csv(request):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)

        

        if request.method == 'POST':
           
            course_id = request.POST['course_id']
            if 'uploadCsvFile' not in request.FILES:
                messages.error(request, 'No file uploaded. Please select a file and try again.')
                return redirect(f'/instructor/courses/each/{course_id}/')
            
            csv_file = request.FILES['uploadCsvFile']
            session_year = request.POST['session_year']
            semester_name = request.POST['semester_name']


            current_session_model = Session.objects.filter(is_current=True).first()
            current_semester_model = Semester.objects.filter(is_current=True).first()

        
            # Check if the uploaded file is a CSV
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a valid CSV file.')
                return redirect(f'/instructor/courses/each/{course_id}/')

            if get_object_or_404(Session, year=session_year) == current_session_model and get_object_or_404(Semester, name=semester_name) == current_semester_model:
                
                try:
                    # Decode the file and process it
                    decoded_file = csv_file.read().decode('utf-8').splitlines()
                    reader = csv.reader(decoded_file)
                    next(reader, None)  # Skip the header row, if it exists

                    for row in reader:

                        print('row', row)
                        # try:
                        registration_id = row[0]
                        grade = row[1]

                        try:
                            # Convert string to UUID
                            reg_uuid = uuid.UUID(registration_id)
                            print(f"Converted UUID: {reg_uuid}")
                        except ValueError as e:
                            print(f"Invalid UUID string: {e}")

                        registration = Registration.objects.filter(id=uuid.UUID(registration_id)).first()

                        result = Result.objects.filter(registration__id=uuid.UUID(registration_id), attempt_number=1).first()

                        if result:
                            # If it exists, update the grade
                            result.grade = int(grade)  # Update the grade field
                            result.save()  # Save the changes
                            print("Existing result updated.")
                        else:
                            # If it doesn't exist, create a new result
                            result = Result.objects.create(
                                registration=registration,
                                attempt_number=1,
                                grade=int(grade)
                            )
                            result.save()
                            print("New result created.")

                    messages.success(request, "CSV file processed successfully.")
                    return redirect(f'/instructor/courses/each/{course_id}/')

                        

                except Result.DoesNotExist:
                    messages.warning(request, f"Registration ID {registration_id} does not exist.")
                except IndexError:
                    messages.error(request, f"Invalid row format: {row}")
                except Exception as e:
                    messages.error(request, f"Error processing row {row}: {e}")

                return redirect(f'/instructor/courses/each/{course_id}/')
            else:
                messages.info(request, f'Can only update current session and semester result!')
                return redirect(f'/instructor/courses/each/{course_id}/')
            
        return redirect("/instructor/courses")
       


@login_required
@user_passes_test(is_instructor, login_url='/404')
def registeredStudentSearchDashboard(request):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        session = Session.objects.all()
        if request.method == "POST":
            matricNo = request.POST["matricNo"]
            sess = request.POST["session"]
            semes = request.POST["semester"]

            if sess != "" and semes != "" and matricNo != "":
                sess = get_object_or_404(Session, year=sess)
                semes = get_object_or_404(Semester, name=semes)
            messages.info(request, f'Fields cannot be empty!')
            redirect(f"instructor/student/search/")


    return render(request, 'admin/student_management_search.html', {"department": instructor.department, 'session': session})


@login_required
@user_passes_test(is_instructor, login_url='/404')
def registeredStuManagementDashboard(request):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        current_session = Session.objects.filter(is_current=True).first()
        
        if request.method == "POST":
            matricNo = request.POST["matricNo"].strip()
            if matricNo != "":
                try:
                    student = Student.objects.all().filter(Q(matricNumber=matricNo) | Q(jambNumber=matricNo), department=instructor.department)
                    if student.exists():
                        stu = student.first()
                        registers = Registration.objects.all().filter(student=get_object_or_404(Student, matricNumber=stu.matricNumber))
                        reg_levels = []
                        for x in registers:
                            reg_levels.append(x.level.name)
                        course_levels.sort(key=int)
                        course_levels = list(set(course_levels))
                        
                        return render(request, 'admin/student_dashboard.html', {"department": instructor.department, 'student': stu, 'registers': registers})
                except:
                    messages.info(request, f'Student not available')
                    return redirect("/instructor/student/management/")
            messages.info(request, f'Field cannot be empty!')
            redirect(f"/instructor/student/management/")

    return render(request, 'admin/student_dashboard.html', {"department": instructor.department, 'curr_sess': current_session})

def F404(request):
    
    return render(request, "admin/404.html")


@login_required
@user_passes_test(is_instructor, login_url='/404')
def registeredStudentManagementDashboard(request):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        current_session = Session.objects.filter(is_current=True).first()
        current_semester = Semester.objects.filter(is_current=True).first()
        if request.method == "POST":
            matricNo = request.POST["matricNo"].strip()
            if matricNo != "":
                try:
                    student = Student.objects.all().filter(Q(matricNumber=matricNo) | Q(jambNumber=matricNo), department=instructor.department).first()
                    
                    if student:
                        
                        enrollment = Enrollment.objects.filter(student=student).order_by('enrolled_date').first()
                        
                        if not enrollment:
                            # Handle case where the student has no enrollment record
                            messages.info(request, f'No enrollment found!')
                            redirect(f"/instructor/student/management/")
                            
                        enrollment_year = int(enrollment.session.year.split('/')[0])
                        
                        # Query all registrations for the student and annotate each session with the calculated level
                        registrations = Registration.objects.filter(student=student).select_related('session')
                        # results = Result.objects.filter(student=student).select_related('registration__session')
                        
                        # Calculate level for each session
                        sessions_and_levels = []
                        for registration in registrations:
                            res = Result.objects.filter(registration__id=registration.id).order_by('-attempt_number').first()
                            print('regis', res)
                            session_year = int(registration.session.year.split('/')[0])
                            # Calculate the difference in years
                            years_since_enrollment = session_year - enrollment_year
                            # Calculate the level, assuming the student starts at Level 100 and progresses yearly
                            current_level = 100 + (years_since_enrollment * 100)
                            
                            sessions_and_levels.append({
                                'session': registration.session.year,
                                'level': current_level,
                                'registration': registration,  # Add any course details if necessary
                                'result': res,
                            })

                        unique_sessions = sorted({entry['session'] for entry in sessions_and_levels})
                        
                        

                        unique_levels = sorted({entry['level'] for entry in sessions_and_levels})

                        courses = Course.objects.all()

                        duration = 0
                        if len(unique_levels) == len(unique_sessions):
                            duration = len(unique_levels)
                        

                        context = {
                            'student': student,
                            'sessions_and_levels': sessions_and_levels,
                        }

                        
                        return render(request, 'admin/student_dashboard.html', {"department": instructor.department, 'curr_sess': current_session, 'curr_semes': current_semester, 'student': student,
                            'sessions_and_levels': sessions_and_levels, 'unique_sessions': unique_sessions, 'unique_levels': unique_levels, 'duration':duration, 'courses': courses, 'matricNo': matricNo})
                except Exception as e:
                    messages.info(request, f'Student not available {e}')
                    return redirect(f"/instructor/student/management/")

            messages.info(request, f'Field cannot be empty!')
            redirect(f"/instructor/student/management/")
    return render(request, 'admin/student_dashboard.html', {"department": instructor.department, 'curr_sess': current_session, 'curr_semes': current_semester})



@login_required
@user_passes_test(is_instructor, login_url='/404')
def studentGradeUpdate(request):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        if request.method == "POST":
            registrationIdInput = request.POST["registrationIdInput"].strip()
            courseGrade = request.POST["course_grade"]

            # register = Registration.objects.all().filter(id=registrationIdInput).first()

            try:
                latest_result = Result.objects.filter(registration__id=registrationIdInput).order_by('-attempt_number').first()

                # Add a new result for the resit
                resit_result = Result.objects.create(
                    registration=get_object_or_404(Registration, id=registrationIdInput),
                    attempt_number=latest_result.attempt_number + 1,
                    grade=float(courseGrade),  # Example resit grade
                )

                # register.grade = courseGrade
                # register.save()

                messages.info(request, f'{latest_result.registration.course.title} grade updated!')
                # requests.post('http://127.0.0.1:8000/target-endpoint/', data=data)
                redirect(f"/instructor/student/management/")
            except Exception as e:
                messages.info(request, f'result not uploaded yet')
                # requests.post('http://127.0.0.1:8000/target-endpoint/', data=data)
                redirect(f"/instructor/student/management/")


    return render(request, 'admin/student_dashboard.html')

@login_required
@user_passes_test(is_instructor, login_url='/404')
def deleteStudentRegisteredCourse(request, id):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()
    try:
        regObjects = Registration.objects.filter(id=id)[0]
        print("1", regObjects.course.title)
        if regObjects.session == current_session_model and regObjects.semester == current_semester_model and regObjects.instructor_remark != 'approved':
            if Registration.objects.all().filter(id=id).exists():
                messages.info(request, f'{regObjects.course.title} deleted successfully')
                regObjects= Registration.objects.filter(id=id).delete()
                
                return redirect("/instructor/student/management/")
            messages.info(request, f'Registered Course not available')
            return redirect("/instructor/student/management/")
        messages.info(request, f'Cannot perform Opereation')
        return redirect("/instructor/student/management/")
    except:
        messages.info(request, f'Registered Course not available')
        return redirect("/instructor/student/management/")

@login_required
@user_passes_test(is_instructor, login_url='/404')
def addCourseStudentRegisteredCourse(request, matricNo):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        try:
            student = Student.objects.all().filter(Q(matricNumber=matricNo) | Q(jambNumber=matricNo), department=instructor.department).first()
            if student:
                courseId = request.GET['course']
                curr_semester = request.GET['curr_semester']
                
                curr_session = request.GET['curr_session']
                current_session_model = Session.objects.filter(is_current=True).first()
                current_semester_model = Semester.objects.filter(is_current=True).first()
                print('semester', curr_semester, current_semester_model , type(curr_semester), type(current_semester_model), curr_semester==current_semester_model)
                print('session', curr_session, current_session_model , type(curr_session), type(current_session_model), curr_session==current_session_model)

                if curr_session == current_session_model.year and curr_semester == current_semester_model.name:
                    course = get_object_or_404(Course, id=courseId)

                    if course.semester.name != current_semester_model.name:
                        messages.info(request, f'Invalid course to enter')
                        return redirect("/instructor/student/management/")
                    
                    if Registration.objects.all().filter(student=student, 
                                                    course=get_object_or_404(Course, id=courseId), 
                                                    session=get_object_or_404(Session, year=curr_session),
                                                    semester=get_object_or_404(Semester, name=curr_semester)).exists():
                        messages.info(request, f'Already registered')
                        return redirect("/instructor/student/management/")

                    course_exist = Registration.objects.create(
                        student=student,
                        course=get_object_or_404(Course, id=courseId),
                        session=get_object_or_404(Session, year=curr_session),
                        semester=get_object_or_404(Semester, name=curr_semester),
                    )
                    course_exist.save()
                    messages.info(request, f'Course Updated')
                    return redirect("/instructor/student/management/")
                messages.info(request, f'Something went wrong!!')
                return redirect("/instructor/student/management/")
            messages.info(request, f'Student does not exist')
            return redirect("/instructor/student/management/")
        except:
            messages.info(request, f'Something went wrong')
            return redirect("/instructor/student/management/")
            

@login_required
@user_passes_test(is_instructor, login_url='/404')
def ApproveRejectReg(request, stats, id):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()

        try:
            print(stats)
            if stats == 'approved' or stats == 'rejected':
                reg = Registration.objects.filter(id=id).first()
                if reg.session == current_session_model and reg.semester == current_semester_model:
                    reg.instructor_remark = stats
                    reg.save()
                    messages.info(request, f'Registered Course {stats}!!')
                    return redirect("/instructor/student/management/")
                else:
                    messages.info(request, f'Request not allowed')
                    return redirect("/instructor/student/management/")
            else:
                messages.info(request, f'Invalid request')
                return redirect("/instructor/student/management/")      
        except:
            messages.info(request, f'Registered Course not available')
            return redirect("/instructor/student/management/")
    return render(request, 'admin/student_dashboard.html')

def login_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = auth.authenticate(username=email, password=password)
            # user = User.objects.get(email=email)
            # if user.check_password(password):
            #     # Log the user in (assuming you're using Django's session framework)
            #     # login(request, user)
            #     return redirect('/')  # Redirect to the dashboard or homepage
            # else:
            #     error_message = "Invalid password."
            if user is not None:
                auth.login(request, user)
                if user.user_type == "student":
                    return redirect("/")
                elif user.user_type == "instructor":
                    return redirect("/instructor/dashboard")
                else:
                    # Redirect user to a 404 page
                    return redirect("/404")
            # elif user is not None and user.user_type == 'student':
            else:
                error_message = "Invalid credentials!"
                messages.info(request, f'Invalid credentials!')
                # return redirect('/accounts/login')
                return render(request, "authentication/login.html", {"error": error_message})
        except User.DoesNotExist:
            error_message = "Invalid credentials!"
            messages.info(request, f'Invalid credentials!')
            # return redirect('/accounts/login')
            return render(request, "authentication/login.html", {"error": error_message})

        return render(request, "login.html", {"error": error_message})

    return render(request, "authentication/login.html")

@login_required
@user_passes_test(is_instructor, login_url='/404')
def manageAddStudent(request):
    if request.user.is_authenticated:
        user = request.user
        instructor = get_object_or_404(Instructor, user=user)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()

        if request.method == 'POST':
            file = request.FILES.get('file')
            
            if not file:
                messages.error(request, "Please upload a file.")
                return redirect('/instructor/add_student/')
            
            try:
                # Load file into a DataFrame (supports CSV/Excel)
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(file)
                else:
                    messages.error(request, "Unsupported file format. Please upload a CSV or Excel file.")
                    return redirect('/instructor/add_student/')

                # Validate required columns
                required_columns = ['surname', 'otherNames', 'currentLevel', 'entryLevel', 'matricNumber', 
                                    'jambNumber', 'dateOfBirth', 'gender', 'studentPhoneNumber',
                                    'college', 'department', 'programme', 'primaryEmail', 'studentEmail',
                                    'modeOfEntry', 'degree', 'currentSession']
                for column in required_columns:
                    if column not in df.columns:
                        messages.error(request, f"Missing required column: {column}")
                        return redirect('/instructor/add_student/')

                # Start a database transaction
                with transaction.atomic():
                    for _, row in df.iterrows():
                        # Fetch related foreign key objects
                        print('row', row)
                        college = College.objects.get(name=row['college'])
                        department = Department.objects.get(name=row['department'])
                        programme = Programme.objects.get(name=row['programme'])
                        session = Session.objects.get(year=row['currentSession'])

                        print('date', row['dateOfBirth'], datetime.strptime(row['dateOfBirth'], "%m/%d/%Y").strftime("%Y-%m-%d"))

                        # Create a CustomUser (assuming email is primary key)
                        user, created = CustomUser.objects.get_or_create(
                            email=row['primaryEmail'],
                            defaults={
                                'username': row['primaryEmail'],
                                'first_name': row['otherNames'],
                                'last_name': row['surname'],
                                'user_type': 'student',
                            }
                        )

                        user.set_password(row['surname'].lower())
                        user.save()

                        # Create or update a Student record
                        student, created = Student.objects.update_or_create(
                            user=user,
                            defaults={
                                'otherNames': row['otherNames'],
                                'surname': row['surname'],
                                'currentLevel': row['currentLevel'],
                                'entryLevel': row['entryLevel'],
                                'currentSession':  current_session_model.year,
                                'matricNumber': row['matricNumber'],
                                'jambNumber': row['jambNumber'],
                                'dateOfBirth': datetime.strptime(row['dateOfBirth'], "%m/%d/%Y").strftime("%Y-%m-%d"),
                                'gender': row['gender'],
                                'studentPhoneNumber': row['studentPhoneNumber'],
                                'college': college,
                                'department': department,
                                'programme': programme,
                                'primaryEmail': row['primaryEmail'],
                                'degree': row['degree'],
                                'modeOfEntry': row['modeOfEntry'],
                                'studentEmail': row['studentEmail'],
                            }
                        )

                        
                    
                    messages.success(request, "Students added successfully.")
                    return redirect('/instructor/add_student/')

            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect('/instructor/add_student/')

        return render(request, 'admin/add_student.html')


@login_required
@user_passes_test(is_advisor, login_url='/404')
def AdvisorDashboard(request):
    if request.user.is_authenticated:
        user = request.user
        advisor = get_object_or_404(LevelAdvisor, user=user)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()

        total_students = len(Student.objects.filter(currentLevel=advisor.level))
        pending_reg = Registration.objects.filter(student__department=advisor.department, student__currentLevel=advisor.level, session=current_session_model,
         semester=current_semester_model, instructor_remark='pending')
        rejected_reg = Registration.objects.filter(student__department=advisor.department, student__currentLevel=advisor.level, session=current_session_model,
         semester=current_semester_model, instructor_remark='rejected')

        # pending_students = Registration.objects.filter(
        #     course__department=advisor.department,
        #     session=current_session_model,
        #     semester=current_semester_model,
        #     instructor_remark='pending'
        # ).values('student').distinct()

        # # If you want actual Student objects:
        # unique_pending_students = Student.objects.filter(
        #     id__in=[entry['student'] for entry in pending_students]
        # )

        pending_students = Student.objects.filter(
            registration__course__department=advisor.department,
            registration__student__currentLevel=advisor.level,
            registration__session=current_session_model,
            registration__semester=current_semester_model,
            registration__instructor_remark='pending'
        ).distinct()

        return render(request, "levelAdvisor/dashboard.html", {'totalStudents': total_students,
                                                                'totalPendingReg': len(pending_reg),
                                                                'level': advisor.level,
                                                                'pendingReg': pending_students,
                                                                'totalRejectedReg': len(rejected_reg)})

@login_required
@user_passes_test(is_advisor, login_url='/404')
def StudentList(request):
    if request.user.is_authenticated:
        user = request.user
        advisor = get_object_or_404(LevelAdvisor, user=user)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()
        courses = Course.objects.all()

        if request.method == "POST":
            matricNo = request.POST["matricNo"].strip()
            if matricNo != "":
                try:
                    student = Student.objects.all().filter(Q(matricNumber=matricNo) | Q(jambNumber=matricNo), department=advisor.department, currentLevel=advisor.level, currentSession=current_session_model.year).first()
                    
                    if student:
                        student_data = []

                        
                        registrations = Registration.objects.filter(
                            student=student,
                            session=current_session_model,
                            semester=current_semester_model,
                        )
                        approved_count = registrations.filter(instructor_remark="approved").count()
                        pending_count = registrations.filter(instructor_remark="pending").count()

                        # Append the data
                        student_data.append({
                            "student": student,
                            "approved_courses": approved_count,
                            "pending_courses": pending_count,
                        })
                
                        return render(request, 'levelAdvisor/student.html', {'student_data': student_data, 
                                                                            'curr_sess': current_session_model,
                                                                            'curr_semes': current_semester_model})
                    else:
                        messages.error(request, f"Student not found!")
                        return redirect('/advisor/students/')
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
                    return redirect('/advisor/students/')
                    
        
        students = Student.objects.filter(
            department=advisor.department,
            currentLevel=advisor.level,
            currentSession=current_session_model.year
        )

        print("students", students)

        student_data = []

        for student in students:
            # Get the registrations for the current session and semester
            registrations = Registration.objects.filter(
                student=student,
                session=current_session_model,
                semester=current_semester_model,
            )
            approved_count = registrations.filter(instructor_remark="approved").count()
            pending_count = registrations.filter(instructor_remark="pending").count()

            # Append the data
            student_data.append({
                "student": student,
                "approved_courses": approved_count,
                "pending_courses": pending_count,
            })

        


    
        return render(request, 'levelAdvisor/student.html', {'student_data': student_data, 
                                                            'curr_sess': current_session_model,
                                                            'curr_semes': current_semester_model})


        students = Student.objects.filter(
            department=advisor.department,
            currentLevel=advisor.level,
            currentSession=current_session_model.year
        )

        print("students", students)
        
        student_data = []
        for student in students:
            # Get the registrations for the current session and semester
            registrations = Registration.objects.filter(
                student=student,
                session=current_session_model,
                semester=current_semester_model,
            )
            approved_count = registrations.filter(instructor_remark="approved").count()
            pending_count = registrations.filter(instructor_remark="pending").count()

            # Append the data
            student_data.append({
                "student": student,
                "approved_courses": approved_count,
                "pending_courses": pending_count,
            })

        


    
        return render(request, 'levelAdvisor/student.html', {'student_data': student_data, 
                                                            'curr_sess': current_session_model,
                                                            'curr_semes': current_semester_model})
    
@login_required
@user_passes_test(is_advisor, login_url='/404')
def AdvisorReg(request):
    if request.user.is_authenticated:
        user = request.user
        advisor = get_object_or_404(LevelAdvisor, user=user)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()
        courses = Course.objects.all()

        matricNo = request.GET.get('q')
    
        if matricNo != "":
            # try:
            student = Student.objects.all().filter(Q(matricNumber=matricNo) | Q(jambNumber=matricNo), department=advisor.department, currentLevel=advisor.level).first()
            print("got here student")
            if student:
                
                
                enrollment = Enrollment.objects.filter(student=student).order_by('enrolled_date').first()
                
                if not enrollment:
                    # Handle case where the student has no enrollment record
                    messages.info(request, f'No enrollment found!')
                    redirect(f"/advisor/reg/")
                    
                enrollment_year = int(enrollment.session.year.split('/')[0])
                
                
                registrations = Registration.objects.filter(student__department=advisor.department, student=student, semester=current_semester_model, session=current_session_model)
                
                
                
                return render(request, 'levelAdvisor/studentManagement.html', {"department": advisor.department, 'curr_sess': current_session_model, 'curr_semes': current_semester_model, 'student': student,
                        'matricNo': matricNo, 'courses': courses, 'registrations': registrations})
            # except Exception as e:
            #     messages.info(request, f'Student not available {e}')
            #     return redirect(f"/advisor/reg/")

        messages.info(request, f'Field cannot be empty!')
        redirect(f"/advisor/reg/")
    return render(request, 'levelAdvisor/studentManagement.html', {"department": advisor.department, 'curr_sess': current_session_model, 'curr_semes': current_semester_model})


@login_required
@user_passes_test(is_advisor, login_url='/404')
def AdvisorDeleteStudentRegisteredCourse(request, id, matricNo):
    if request.user.is_authenticated:
        user = request.user
        advisor = get_object_or_404(LevelAdvisor, user=user)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()
    try:
        regObjects = Registration.objects.filter(id=id)[0]
        if regObjects.session == current_session_model and regObjects.semester == current_semester_model and regObjects.instructor_remark != 'approved':
            if Registration.objects.all().filter(id=id).exists():
                messages.info(request, f'{regObjects.course.title} deleted successfully')
                regObjects= Registration.objects.filter(id=id).delete()
                
                return redirect(f"/advisor/reg/?q={matricNo}")
            messages.info(request, f'Registered Course not available')
            return redirect(f"/advisor/reg/?q={matricNo}")
        messages.info(request, f'Cannot perform Opereation')
        return redirect(f"/advisor/reg/?q={matricNo}")
    except:
        messages.info(request, f'Registered Course not available')
        return redirect(f"/advisor/reg/?q={matricNo}")

@login_required
@user_passes_test(is_advisor, login_url='/404')
def AdvisorAddCourseStudentRegisteredCourse(request, matricNo):
    if request.user.is_authenticated:
        user = request.user
        advisor = get_object_or_404(LevelAdvisor, user=user)
        try:
            student = Student.objects.all().filter(Q(matricNumber=matricNo) | Q(jambNumber=matricNo), department=advisor.department).first()
            if student:
                courseId = request.GET['course']
                curr_semester = request.GET['curr_semester']
                
                curr_session = request.GET['curr_session']
                current_session_model = Session.objects.filter(is_current=True).first()
                current_semester_model = Semester.objects.filter(is_current=True).first()
               
                if curr_session == current_session_model.year and curr_semester == current_semester_model.name:
                    course = get_object_or_404(Course, id=courseId)

                    if course.semester.name != current_semester_model.name:
                        messages.info(request, f'Invalid course to enter')
                        return redirect(f"/advisor/reg/?q={matricNo}")
                    
                    if Registration.objects.all().filter(student=student, 
                                                    course=get_object_or_404(Course, id=courseId), 
                                                    session=get_object_or_404(Session, year=curr_session),
                                                    semester=get_object_or_404(Semester, name=curr_semester)).exists():
                        messages.info(request, f'Already registered')
                        return redirect(f"/advisor/reg/?q={matricNo}")

                    course_exist = Registration.objects.create(
                        student=student,
                        course=get_object_or_404(Course, id=courseId),
                        session=get_object_or_404(Session, year=curr_session),
                        semester=get_object_or_404(Semester, name=curr_semester),
                    )
                    course_exist.save()
                    messages.info(request, f'Course Updated')
                    return redirect(f"/advisor/reg/?q={matricNo}/")
                messages.info(request, f'Something went wrong!!')
                return redirect(f"/advisor/reg/?q={matricNo}")
            messages.info(request, f'Student does not exist')
            return redirect(f"/advisor/reg/?q={matricNo}")
        except:
            messages.info(request, f'Something went wrong')
            return redirect(f"/advisor/reg/?q={matricNo}")
            

@login_required
@user_passes_test(is_advisor, login_url='/404')
def AdvisorApproveRejectReg(request, stats, id, matricNo):
    if request.user.is_authenticated:
        user = request.user
        advisor = get_object_or_404(LevelAdvisor, user=user)
        current_session_model = Session.objects.filter(is_current=True).first()
        current_semester_model = Semester.objects.filter(is_current=True).first()

        try:
            if stats == 'approved' or stats == 'rejected':
                reg = Registration.objects.filter(id=id).first()
                if reg.session == current_session_model and reg.semester == current_semester_model:
                    reg.instructor_remark = stats
                    reg.save()
                    messages.info(request, f'Registered Course {stats}!!')
                    return redirect(f"/advisor/reg/?q={matricNo}")
                else:
                    messages.info(request, f'Request not allowed')
                    return redirect(f"/advisor/reg/?q={matricNo}")
            else:
                messages.info(request, f'Invalid request')
                return redirect(f"/advisor/reg/?q={matricNo}")      
        except:
            messages.info(request, f'Registered Course not available')
            return redirect(f"/advisor/reg/?q={matricNo}")
    return render(request, 'advisor/studentManagement.html')



@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")


def get_latest_failed_or_pending_courses(student):
    # Step 1: Get the current semester and session
    try:
        current_semester = Semester.objects.get(is_current=True)
        current_session = Session.objects.get(is_current=True)
    except ObjectDoesNotExist as e:
        raise ValueError("Ensure both the current semester and session are set.") from e

    # Step 2: Filter all registrations for the student
    registrations = Registration.objects.filter(student=student)

    # Step 3: Annotate courses with the latest registration date
    annotated_courses = registrations.annotate(latest_registration_date=Max('registration_date'))

    # Step 4: Filter for courses with the latest registration date
    latest_registrations = annotated_courses.filter(
        registration_date=F('latest_registration_date')
    )

    # Step 5: Filter pending or failed courses that are not in the current semester or session
    filtered_courses = latest_registrations.filter(
        Q(grade_remark__in=['pending', 'failed']),
    #     ~Q(semester=current_semester),
    #     ~Q(session=current_session)
    )

    return filtered_courses