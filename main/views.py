from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import csv
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegistrationForm, FeedbackForm, InquiryForm, FloorPlanForm
from .models import CustomUser, Feedback, Inquiry, FloorPlan, Gallery


# Function to check if the user is an employee
def is_employee(user):
    return user.role == CustomUser.EMPLOYEE


# Register View
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('client_dashboard')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


# Login View
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('employee_dashboard' if user.role == CustomUser.EMPLOYEE else 'client_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')


# Client Dashboard View
@login_required
def client_dashboard(request):
    feedbacks = Feedback.objects.filter(user=request.user)
    inquiries = Inquiry.objects.filter(user=request.user)
    return render(request, 'client_dashboard.html', {'feedbacks': feedbacks, 'inquiries': inquiries})


# Employee Dashboard View
@login_required
@user_passes_test(is_employee, login_url='client_dashboard')
def employee_dashboard(request):
    return render(request, 'employee_dashboard.html')


# Feedback Submission View
@login_required
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('feedback_success')
    else:
        form = FeedbackForm()
    return render(request, 'submit_feedback.html', {'form': form})


# Feedback Success Page View
def feedback_success(request):
    return render(request, 'feedback_success.html')


# Employee Feedback Report View
@login_required
@user_passes_test(is_employee, login_url='client_dashboard')
def feedback_report(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback_report.html', {'feedbacks': feedbacks})


# Employee Delete Feedback
@login_required
@user_passes_test(is_employee, login_url='client_dashboard')
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    feedback.delete()
    return redirect('feedback_report')


# CSV Report Download View (Feedback)
@login_required
@user_passes_test(is_employee, login_url='client_dashboard')
def download_feedback_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="feedback_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Client Name', 'Email', 'Rating', 'Feedback Message', 'Date'])
    for feedback in Feedback.objects.all():
        writer.writerow([feedback.user.username, feedback.user.email, feedback.rating, feedback.message, feedback.created_at])
    return response


# Submit Inquiry (Client)
@login_required
def submit_inquiry(request):
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.user = request.user
            inquiry.save()
            return redirect('inquiry_success')
    else:
        form = InquiryForm()
    return render(request, 'submit_inquiry.html', {'form': form})


# inquiries view
@login_required
def inquiries_view(request):
    if request.user.role == "Client":
        return render(request, 'client_inquiries.html')  # Replace with the actual template
    else:
        return redirect('inquiry_report')  # Redirect employees to the report page


# feedback view
@login_required
def feedback_view(request):
    if request.user.role == "Client":
        return render(request, 'submit_feedback.html')  # Replace with actual template
    else:
        return redirect('feedback_report')  # Redirect employees to feedback report
    

# Inquiry Success Page
def inquiry_success(request):
    return render(request, 'inquiry_success.html')


# View Inquiry Report (Employee)
@login_required
@user_passes_test(is_employee, login_url='client_dashboard')
def inquiry_report(request):
    inquiries = Inquiry.objects.all()
    return render(request, 'inquiry_report.html', {'inquiries': inquiries})


# Employee Delete Inquiry
@login_required
@user_passes_test(is_employee, login_url='client_dashboard')
def delete_inquiry(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id)
    inquiry.delete()
    return redirect('inquiry_report')


# Download Inquiry Report (CSV)
@login_required
@user_passes_test(is_employee, login_url='client_dashboard')
def download_inquiry_report(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="inquiry_report.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Email', 'Subject', 'Inquiry Message', 'Date Submitted'])
    for inquiry in Inquiry.objects.all():
        writer.writerow([inquiry.user.username, inquiry.user.email, inquiry.subject, inquiry.message, inquiry.created_at])
    return response


# Upload Floor Plan
@login_required
@user_passes_test(is_employee, login_url='client_dashboard')
def upload_floor_plan(request):
    if request.method == 'POST':
        form = FloorPlanForm(request.POST, request.FILES)
        if form.is_valid():
            floor_plan = form.save(commit=False)
            floor_plan.uploaded_by = request.user
            floor_plan.save()
            return redirect('floor_plan_list')
    else:
        form = FloorPlanForm()
    return render(request, 'upload_floor_plan.html', {'form': form})


# List & Search Floor Plans
@login_required
@user_passes_test(is_employee, login_url='client_dashboard')
def floor_plan_list(request):
    query = request.GET.get('q', '')
    floor_plans = FloorPlan.objects.filter(title__icontains=query) if query else FloorPlan.objects.all()
    return render(request, 'floor_plan_list.html', {'floor_plans': floor_plans, 'query': query})


# Delete Floor Plan
@login_required
@user_passes_test(is_employee, login_url='client_dashboard')
def delete_floor_plan(request, floor_plan_id):
    floor_plan = get_object_or_404(FloorPlan, id=floor_plan_id)
    floor_plan.delete()
    return redirect('floor_plan_list')


# Floor Plans (Updated)
@login_required
@user_passes_test(lambda u: u.role == CustomUser.EMPLOYEE, login_url='client_dashboard')
def floor_plans(request):
    return render(request, 'floor_plans.html')


# Gallery View
def gallery_view(request):
    images = Gallery.objects.all()
    return render(request, 'gallery.html', {'images': images})


# Home View (Add this to match the paths)
def home(request):
    return render(request, 'home.html')


# Services View
def services(request):
    return render(request, 'services.html')


# About Us
def about(request):
    return render(request, 'about.html')