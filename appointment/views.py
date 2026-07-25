
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Timeslot
from datetime import date, timedelta
import calendar

def staff_schedule_view(request):

    # staff side view: shows BOOKED timeslots so staff can work the day
    # this is the mirror of schedule_view — same pattern, but is_booked=True

    # anchor date defaults to today; bad input falls back to today
    anchor = request.GET.get('date')
    try:
        anchor_date = date.fromisoformat(anchor) if anchor else timezone.localdate()
    except ValueError:
        anchor_date = timezone.localdate()

    # toggle defaults to day view
    view_mode = request.GET.get('view', 'day')

    # date range from the toggle
    if view_mode == 'week':
        start = anchor_date - timedelta(days=anchor_date.weekday())  # monday
        end = start + timedelta(days=6)
    elif view_mode == 'month':
        start = anchor_date.replace(day=1)
        last_day = calendar.monthrange(anchor_date.year, anchor_date.month)[1]
        end = anchor_date.replace(day=last_day)
    else:  # day
        start = anchor_date
        end = anchor_date

    # pull booked slots inside the range, earliest first
    booked_slots = Timeslot.objects.filter(
        is_booked=True,
        date__gte=start,
        date__lte=end,
    ).order_by('date', 'start_time')

    return render(request, 'scheduling/staff_schedule.html', {
        'booked_slots': booked_slots,
        'anchor_date': anchor_date,
        'view_mode': view_mode,
        'range_start': start,
        'range_end': end,
    })

def dashboard_view(request):
    return render(request, 'scheduling/dashboard.html')

def schedule_view(request):

    #searches SQLite3 database for available timeslots
    available_slots = Timeslot.objects.filter(
        is_booked=False,
        date__gte=timezone.localdate()
    ).order_by('date', 'start_time')

    #returns all available appointments if data selected, defaults to first 7 timeslots
    selected_date = request.GET.get('date')
    if selected_date:
        available_slots = available_slots.filter(date=selected_date)
    else:
        available_slots = available_slots[:7]

    #returns available timeslots for rendering and re-renders selected date
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