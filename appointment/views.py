
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from .models import Timeslot
from datetime import date, timedelta
import calendar
from django.urls import reverse
from urllib.parse import urlencode
from .models import Timeslot, IntakeForm
from .forms import IntakeFormForm
from accounts.models import Patient


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

    ### Shows all appts for staff and only user's appts for user
    if request.user.is_staff:
        booked_slots = Timeslot.objects.filter(
            is_booked=True,
            date__gte=start,
            date__lte=end,
            status='scheduled',
        ).order_by('date', 'start_time')

    else:
        booked_slots = Timeslot.objects.filter(
            is_booked=True,
            date__gte=start,
            date__lte=end,
            booked_appt_id__user=request.user,
            status='scheduled',
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

    #re-hydrates the previously selected patient so it survives the date form's GET submit
    #non-staff can only ever book for themselves, so their patient_id is fixed server-side
    #rather than trusted from the querystring
    if request.user.is_staff:
        selected_patient_id = request.GET.get('patient_id')
    else:
        selected_patient_id = getattr(getattr(request.user, 'patient', None), 'patient_id', None)

    selected_patient = None
    if selected_patient_id:
        selected_patient = Patient.objects.filter(patient_id=selected_patient_id).first()

    #returns available timeslots for rendering and re-renders selected date
    return render(request, 'scheduling/schedule.html', {
        'available_slots': available_slots,
        'selected_date': selected_date,
        'selected_patient': selected_patient,
        'effective_patient_id': selected_patient_id,
    })


def confirmation_view(request, slot_id):

    slot = get_object_or_404(Timeslot, id=slot_id)

    return render(request, 'scheduling/confirmation.html', {
        'slot': slot
    })


def intake_form_view(request, slot_id):

    slot = get_object_or_404(Timeslot, id=slot_id)

    # if this slot already has an intake, load it so the student edits
    # instead of creating a second one (the OneToOne would crash on a dupe)
    existing = IntakeForm.objects.filter(timeslot=slot).first()

    if request.method == "POST":
        form = IntakeFormForm(request.POST, instance=existing)
        if form.is_valid():
            intake = form.save(commit=False)  # hold it before hitting the db
            intake.timeslot = slot            # attach it to this slot
            intake.save()
        return redirect('appointment:dashboard')
    else:
        form = IntakeFormForm(instance=existing)

    return render(request, 'scheduling/intake_form.html', {
        'form': form,
        'slot': slot,
    })


def save_appt(request):

    if request.method == "POST":

        slot_id = request.POST.get("slot_id")
        patient_id = request.POST.get("patient_id")

        print("Saving appt slot: ", slot_id)
        print("For patient: ", patient_id)

        timeslot = get_object_or_404(Timeslot, id=slot_id)

        timeslot.is_booked = True
        timeslot.booked_appt_id = Patient.objects.get(patient_id=patient_id)

        timeslot.save()

        return redirect('appointment:confirmation', slot_id)

    else:
        return redirect('appointment:schedule_page')

# each status maps to the list of statuses it's allowed to move to.
# the three end states map to empty lists, so nothing can leave them.
ALLOWED_TRANSITIONS = {
    "scheduled":  ["checked_in", "cancelled", "no_show"],
    "checked_in": ["completed", "cancelled"],
    "completed":  [],
    "cancelled":  [],
    "no_show":    [],
}


def update_status(request):

    if request.method == "POST":

        slot_id = request.POST.get("slot_id")
        new_status = request.POST.get("status")

        timeslot = get_object_or_404(Timeslot, id=slot_id)

        current_status = timeslot.status

        # only save if the move is allowed out of the current status.
        # an illegal move is skipped, so the old status stays put.
        if new_status in ALLOWED_TRANSITIONS.get(current_status, []):
            timeslot.status = new_status
            timeslot.save()

        # bounce back to the same day/view they were looking at
        params = urlencode({
            "date": request.POST.get("date", ""),
            "view": request.POST.get("view", "day"),
        })
        return redirect(f"{reverse('appointment:staff_schedule')}?{params}")

    else:
        return redirect('appointment:staff_schedule')