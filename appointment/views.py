"""this is where your typical "python" logic will go"""

from django.shortcuts import render
from django.utils import timezone

from .models import Timeslot

# Create your views here.
def dashboard_view(request):
    return render(request, 'scheduling/dashboard.html')

def schedule_view(request):
    available_slots = Timeslot.objects.filter(
        is_booked=False,
        date__gte=timezone.localdate()
    ).order_by('date', 'start_time')

    selected_date = request.GET.get('date')
    if selected_date:
        available_slots = available_slots.filter(date=selected_date)
    else:
        available_slots = available_slots[:7]

    return render(request, 'scheduling/schedule.html', {
        'available_slots': available_slots,
        'selected_date': selected_date,
    })

def confirmation_view(request):
    return render(request, 'scheduling/confirmation.html')