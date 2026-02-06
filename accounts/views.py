"""
Hospital Management - Accounts App Views

Authentication and dashboard views.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy

from .forms import PatientRegistrationForm, DoctorRegistrationForm, UserLoginForm
from .decorators import patient_required, doctor_required
def dashboard(request):

    if request.user.is_authenticated:

        if not hasattr(request.user, 'profile'):
            from .models import UserProfile
            UserProfile.objects.create(user=request.user, role='PATIENT')

        if request.user.profile.is_doctor:
            return redirect('doctors:dashboard')

        elif request.user.profile.is_admin or request.user.is_staff:
            return redirect('/admin/')

    return redirect('doctors:doctor_list')


class PatientRegisterView(CreateView):
    """Patient registration view."""
    form_class = PatientRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user)  <-- Remove auto-login
        messages.success(self.request, 'Registration successful! Please log in to continue.')
        return redirect(self.success_url)


class DoctorRegisterView(CreateView):
    """Doctor registration view - creates User, Doctor profile, redirects to doctor dashboard."""
    form_class = DoctorRegistrationForm
    template_name = 'accounts/doctor_register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()
        # login(self.request, user) <-- Remove auto-login
        messages.success(self.request, 'Registration successful. Please log in to continue.')
        return redirect(self.success_url)


class UserLoginView(LoginView):
    """User login view."""
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


def user_logout(request):
    """User logout view."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

def location_page(request):
    """
    Location selection before showing doctors (Swiggy style).
    """

    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.method == "POST":
        pincode = request.POST.get("pincode")
        request.session['pincode'] = pincode
        return redirect('doctors:doctors_list')

    return render(request, "location.html")
