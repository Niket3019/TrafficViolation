from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Violation, Grievance, Account
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Account,UploadedImage  # Ensure you have an Account model
import os
import subprocess
import sys
from django.http import JsonResponse
from violation_app.services import email
from django.urls import reverse

@csrf_exempt
def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        vehicle_no = request.POST["vehicle_no"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists!")
        elif password1 != password2:
            messages.error(request, "Passwords do not match!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            Account.objects.create(user=user, vehicle_number=vehicle_no)
            user.save()
            messages.success(request, "Registered successfully!")
            return redirect("login")

    return render(request, "register.html")

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']  # Get selected role

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if role == 'admin' and user.is_staff:  # Admin Login
                login(request, user)
                return redirect('admin_dashboard')
            elif role == 'user' and not user.is_staff:  # User Login
                login(request, user)
                return redirect('user_dashboard')
            else:
                messages.error(request, "Invalid role selection for this user.")
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

@csrf_exempt
def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")
    violations = Violation.objects.filter(user=request.user)
    return render(request, "user_dashboard.html", {"violations": violations})

@csrf_exempt
def pay_fine(request, violation_id):
    violation = get_object_or_404(Violation, id=violation_id)
    violation.is_paid = True
    violation.save()
    messages.success(request, "Fine paid successfully!")
    return redirect("user_dashboard")

@csrf_exempt
def file_grievance(request, violation_id):
    violation = get_object_or_404(Violation, id=violation_id)
    if request.method == "POST":
        complaint_text = request.POST["reason"]
        Grievance.objects.create(user=request.user, violation=violation, complaint_text=complaint_text)
        messages.success(request, "Grievance submitted!")
        return redirect("user_dashboard")
    return render(request, "grievance.html", {"violation": violation})
csrf_exempt
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")
csrf_exempt
@login_required
def admin_dashboard(request):
    violations = Violation.objects.all().order_by('-created_at')
    grievances = Grievance.objects.all()
    users = Account.objects.all()
    uploaded_images = UploadedImage.objects.exclude(image="").all()
    return render(request, "admin_dashboard.html", {
        "violations": violations,
        "grievances": grievances,
        "users":users,
        "uploaded_images":uploaded_images
    })

@csrf_exempt
@login_required
def send_violation_email(request, violation_id):
    violation = get_object_or_404(Violation, id=violation_id)
    email_id = violation.user.email
    subject = 'Traffic Violation Notice'
    login_url = request.build_absolute_uri(reverse('login'))  # Generates the absolute login URL
    message = (f"Dear {violation.user.username},\n"
               f"You have a violation for {violation.violation_type}. "
               f"Please pay ₹{violation.fine_amount}.\n\n"
               f"To manage your violations, please log in: {login_url}")
    
    email.send_mail_admin(email_id, subject, message)
    messages.success(request, f"Email sent successfully to {email_id}")
    return redirect("admin_dashboard")


@csrf_exempt
@login_required
def update_grievance_status(request):
    if request.method == "POST":
        for grievance in Grievance.objects.all():
            new_status = request.POST.get(f"grievance_status_{grievance.id}")
            if new_status and new_status != grievance.status:
                grievance.status = new_status
                grievance.save()
        messages.success(request, "Grievance status updated successfully!")
    return redirect("admin_dashboard")

@csrf_exempt
@login_required
def add_violation_view(request):
    if request.method == "POST":
        user_id = request.POST["user_id"]
        vehicle_number = request.POST["vehicle_number"]
        violation_type = request.POST["violation_type"]
        fine_amount = request.POST["fine_amount"]
        image_id = request.POST["image_id"]

        selected_image = UploadedImage.objects.get(id=image_id)

        Violation.objects.create(
            user_id=user_id,
            vehicle_number=vehicle_number,
            violation_type=violation_type,
            fine_amount=fine_amount,
            image=selected_image.image
        )
        messages.success(request, "Violation sent to user!")
        return redirect("admin_dashboard")
    return render(request, "admin_dashboard.html")


def open_gui(request):
    """Launch the Tkinter GUI when called"""
    try:
        python_executable = sys.executable  # Get current venv Python
        subprocess.Popen([python_executable, "-m", "violation_app.gui_script"])  # Run as a module
        return JsonResponse({"message": "GUI Opened Successfully!"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def index(request):
    return render(request, "index.html")