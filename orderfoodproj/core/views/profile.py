from django.shortcuts import render, redirect 


def get_profile_view(request):
    return render(request, 'core/profile.html', {})
