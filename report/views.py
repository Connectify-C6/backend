import re
from django.shortcuts import render,redirect
from report.models import Report
from django.contrib.auth.models import User
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from login.models import UserProfile
from django.contrib.auth import logout

def report_user(request, reported_user_id):
    if not request.user.is_authenticated:
        return redirect('login:login_user')
    
    reported_user = get_object_or_404(User, pk=reported_user_id)

    if request.method == 'GET':
        return render(request, 'report_user.html', {'reported_user': reported_user})

    elif request.method == 'POST':
        reporter = request.user
        reported_user = get_object_or_404(User, pk=reported_user_id)
        reason = request.POST.get('reason')
        user_profile = get_user_profile_by_id(reported_user.id)
        user_profile.count_reported += 1
        user_profile.save()
        print(reporter.username)
        print(user_profile.count_reported)
        
        # Check if count_reported exceeds the limit
        if user_profile.count_reported > 5:
            reported_user.delete()
            return redirect(reverse('profile_user:get_profile_by_username', kwargs={'username': reporter.username}))
        # Create a report instance
        report = Report.objects.create(
            reported_user=reported_user,
            reporter=reporter,
            reason=reason
        )
        
        report.save()
        
        return redirect(reverse('profile_user:get_profile_by_username', kwargs={'username': reported_user.username}) + '?report_success=True')
    
def get_user_profile_by_id(user_id):
    try:
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
        return user_profile
    except UserProfile.DoesNotExist:
        return None
    except User.DoesNotExist:
        return None
    
def all_users(request):
    users = User.objects.all()
    return render(request, 'all_users.html', {'users': users})


def view_reports(request):
    reports = Report.objects.all()  # Fetch all reports from the database
    return render(request, 'view_reports.html', {'reports': reports})
