"""
Hospital Management - Role-based access decorators.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def patient_required(view_func):
    """Decorator: user must be logged in with Patient role."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('accounts:login')
        if hasattr(request.user, 'profile') and request.user.profile.is_patient:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access denied. Patient account required.')
        return redirect('accounts:dashboard')
    return wrapper


def doctor_required(view_func):
    """Decorator: user must be logged in with Doctor role."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to access this page.')
            return redirect('accounts:login')
        if hasattr(request.user, 'profile') and request.user.profile.is_doctor:
            return view_func(request, *args, **kwargs)
        messages.error(request, 'Access denied. Doctor account required.')
        return redirect('accounts:dashboard')
    return wrapper
