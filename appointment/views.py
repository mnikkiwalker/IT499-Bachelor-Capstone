"""this is where your typical "python" logic will go"""

from django.shortcuts import render, get_object_or_404, redirect
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

def confirmation_view(request, slot_id):

    slot = get_object_or_404(Timeslot, id=slot_id)

    return render(request, 'scheduling/confirmation.html', {
        'slot': slot
    })

def save_appt(request):

    if request.method == "POST":

        slot_id = request.POST.get("slot_id")

        print("Saving appt slot: ", slot_id)

        timeslot = get_object_or_404(Timeslot, id=slot_id)

        timeslot.is_booked = True

        timeslot.save()

        return redirect('appointment:confirmation', slot_id)

    else:
        return redirect('appointment:schedule_page')