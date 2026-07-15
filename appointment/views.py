"""this is where your typical "python" logic will go"""

from django.shortcuts import render

# Create your views here.
def dashboard_view(request):
    return render(request, 'scheduling/dashboard.html')

def schedule_view(request):
    return render(request, 'scheduling/schedule.html')

def confirmation_view(request):
    return render(request, 'scheduling/confirmation.html')