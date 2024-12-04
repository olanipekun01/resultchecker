from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
# from .forms import UserSignupForm, StudentSignupForm, InstructorSignupForm
from .models import *
from django.db.models import Q
import uuid
import random
import string
import json

import os

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


# @login_required
# @user_passes_test(is_student, login_url="/404")
def Courses(request):


    return render(request, "user/courses.html", {"student": 'student'})

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

# def login_view(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             email = data.get('email')
#             password = data.get('password')

#             # Authenticate user
#             print('data', email, password)
#             user = authenticate(request, username=email, password=password)
#             if user:
#                 auth.login(request, user)
#                 return JsonResponse({'message': 'Login successful'}, status=200)
#             else:
#                 return JsonResponse({'error': 'Invalid email or password'}, status=401)

#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)

#     return render(request, "authentication/login.html")


@login_required
def logout(request):
    auth.logout(request)
    return redirect("/")