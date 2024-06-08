from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.iuhiuhi
from django.shortcuts import render
from .models import Volunteer, FoodBank, Task, IndividualShift, Vehicle, TransitSchedule, FoodItem
from django.db.models import Q

@login_required
def home_view(request):
    return render(request, 'home.html')

def volunteer_view(request):
    volunteers = Volunteer.objects.all()

    query = request.GET.get('q')
    if query:
        volunteers = volunteers.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(street_address__icontains=query) |
            Q(city__icontains=query) |
            Q(home_state__icontains=query) |
            Q(zip_code__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        home_state = request.POST.get('home_state')
        zip_code = request.POST.get('zip_code')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        # Check that at least one field is not empty
        if any([first_name, last_name, street_address, city, home_state, zip_code, phone_number, email]):
            Volunteer.objects.create(
                first_name=first_name,
                last_name=last_name,
                street_address=street_address,
                city=city,
                home_state=home_state,
                zip_code=zip_code,
                phone_number=phone_number,
                email=email
            )
        elif 'edit' in request.POST:
            volunteer_id = request.POST.get('volunteer_id')
            volunteer = Volunteer.objects.get(id=volunteer_id)
            volunteer.first_name = request.POST.get('first_name')
            # Update other fields for editing
            volunteer.save()
        elif 'delete' in request.POST:
            volunteer_id = request.POST.get('volunteer_id')
            Volunteer.objects.get(id=volunteer_id).delete()

        return redirect('volunteer')

    context = {
        'volunteers': volunteers,
        'query': query,
    }
    return render(request, 'volunteer.html', context)

# views.py
from django.shortcuts import render, redirect
from .models import Volunteer

def volunteer_edit_view(request):
    if request.method == 'POST':
        volunteer_id = request.POST.get('volunteer_id')
        volunteer = Volunteer.objects.get(id=volunteer_id)
        volunteer.first_name = request.POST.get('first_name')
        volunteer.last_name = request.POST.get('last_name')
        volunteer.street_address = request.POST.get('street_address')
        volunteer.city = request.POST.get('city')
        volunteer.home_state = request.POST.get('home_state')
        volunteer.zip_code = request.POST.get('zip_code')
        volunteer.phone_number = request.POST.get('phone_number')
        volunteer.email = request.POST.get('email')
        volunteer.save()
        return redirect('volunteer')
    return redirect('home')  # Redirect to home if not a POST request
def volunteer_delete(request):
    if request.method == 'POST':
        volunteer_id = request.POST.get('volunteer_id')
        volunteer = get_object_or_404(Volunteer, id=volunteer_id)
        volunteer.delete()
    return redirect('volunteer')

def foodbank_view(request):
    foodbanks = FoodBank.objects.all()

    query = request.GET.get('q')
    if query:
        foodbanks = foodbanks.filter(
            Q(street_address__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query) |
            Q(phone_number__icontains=query) |
            Q(email__icontains=query)
        )

    if request.method == 'POST':
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        foodbank_id = request.POST.get('foodbank_id')  # Get the ID of the food bank

        if foodbank_id:  # If the ID exists, update the existing entry
            foodbank = FoodBank.objects.get(id=foodbank_id)
            foodbank.street_address = street_address
            foodbank.city = city
            foodbank.state = state
            foodbank.phone_number = phone_number
            foodbank.email = email
            foodbank.save()
        else:  # If the ID does not exist, create a new entry
            FoodBank.objects.create(
                street_address=street_address,
                city=city,
                state=state,
                phone_number=phone_number,
                email=email
            )

        return redirect('foodbank')

    context = {
        'foodbanks': foodbanks,
        'query': query,
    }
    return render(request, 'foodbank.html', context)


def foodbank_delete(request):
    if request.method == 'POST':
        foodbank_id = request.POST.get('foodbank_id')
        foodbank = get_object_or_404(FoodBank, id=foodbank_id)
        foodbank.delete()
    return redirect('foodbank')

def task_view(request):
    tasks = Task.objects.all()
    foodbanks = FoodBank.objects.all()

    query = request.GET.get('q')
    if query:
        tasks = tasks.filter(
            Q(description__icontains=query) |
            Q(start_date_time__icontains=query) |
            Q(end_date_time__icontains=query) |
            Q(associated_food_bank__street_address__icontains=query) |
            Q(min_volunteers__icontains=query) |
            Q(max_volunteers__icontains=query)
        )

    if request.method == 'POST':
        description = request.POST.get('description')
        start_date_time = request.POST.get('start_date_time')
        end_date_time = request.POST.get('end_date_time')
        associated_food_bank_id = request.POST.get('associated_food_bank')
        min_volunteers = request.POST.get('min_volunteers')
        max_volunteers = request.POST.get('max_volunteers')

        task_id = request.POST.get('task_id')  # Get the ID of the task

        if task_id:  # If the ID exists, update the existing entry
            task = Task.objects.get(id=task_id)
            task.description = description
            task.start_date_time = start_date_time
            task.end_date_time = end_date_time
            task.associated_food_bank_id = associated_food_bank_id
            task.min_volunteers = min_volunteers
            task.max_volunteers = max_volunteers
            task.save()
        else:  # If the ID does not exist, create a new entry
            Task.objects.create(
                description=description,
                start_date_time=start_date_time,
                end_date_time=end_date_time,
                associated_food_bank_id=associated_food_bank_id,
                min_volunteers=min_volunteers,
                max_volunteers=max_volunteers
            )

        return redirect('task')

    context = {
        'tasks': tasks,
        'foodbanks': foodbanks,
        'query': query,
    }
    return render(request, 'task.html', context)


def task_delete(request):
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        task.delete()
    return redirect('task')
def individual_shift_view(request):
    shifts = IndividualShift.objects.all()
    volunteers = Volunteer.objects.all()
    tasks = Task.objects.all()

    query = request.GET.get('q')
    if query:
        shifts = shifts.filter(
            Q(volunteer__first_name__icontains=query) |  # Search by volunteer first name
            Q(volunteer__last_name__icontains=query) |   # Search by volunteer last name
            Q(task__description__icontains=query)        # Search by task description
        )

    if request.method == 'POST':
        volunteer_id = request.POST.get('volunteer')
        task_id = request.POST.get('task')

        shift_id = request.POST.get('shift_id')  # Get the ID of the shift

        if shift_id:  # If the ID exists, update the existing entry
            shift = IndividualShift.objects.get(id=shift_id)
            shift.volunteer_id = volunteer_id
            shift.task_id = task_id
            shift.save()
        else:  # If the ID does not exist, create a new entry
            IndividualShift.objects.create(
                volunteer_id=volunteer_id,
                task_id=task_id
            )

        return redirect('individual_shift')

    context = {
        'shifts': shifts,
        'volunteers': volunteers,
        'tasks': tasks,
        'query': query,
    }
    return render(request, 'individual_shift.html', context)


def individual_shift_delete(request):
    if request.method == 'POST':
        shift_id = request.POST.get('shift_id')
        shift = get_object_or_404(IndividualShift, id=shift_id)
        shift.delete()
    return redirect('individual_shift')

def vehicle_view(request):
    vehicles = Vehicle.objects.all()
    volunteers = Volunteer.objects.all()

    query = request.GET.get('q')
    if query:
        vehicles = vehicles.filter(
            Q(driver_volunteer__first_name__icontains=query) |
            Q(driver_volunteer__last_name__icontains=query) |
            Q(vehicle_type__icontains=query)
        )

    if request.method == 'POST':
        vehicle_type = request.POST.get('vehicle_type')
        total_passenger_capacity = request.POST.get('total_passenger_capacity')
        driver_volunteer_id = request.POST.get('driver_volunteer')

        vehicle_id = request.POST.get('vehicle_id')  # Get the ID of the vehicle

        if vehicle_id:  # If the ID exists, update the existing entry
            vehicle = Vehicle.objects.get(id=vehicle_id)
            vehicle.driver_volunteer_id = driver_volunteer_id
            vehicle.vehicle_type = vehicle_type
            vehicle.total_passenger_capacity = total_passenger_capacity
            vehicle.save()
        else:  # If the ID does not exist, create a new entry
            Vehicle.objects.create(
                driver_volunteer_id=driver_volunteer_id,
                vehicle_type=vehicle_type,
                total_passenger_capacity=total_passenger_capacity
            )

        return redirect('vehicle')

    context = {
        'vehicles': vehicles,
        'volunteers': volunteers,
        'query': query,
    }
    return render(request, 'vehicle.html', context)


def vehicle_delete(request):
    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle_id')
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)
        vehicle.delete()
    return redirect('vehicle')

def transit_view(request):
    transit_schedules = TransitSchedule.objects.all()
    vehicles = Vehicle.objects.all()

    query = request.GET.get('q')
    if query:
        transit_schedules = transit_schedules.filter(
            Q(vehicle__driver_volunteer__first_name__icontains=query) |
            Q(vehicle__driver_volunteer__last_name__icontains=query) |
            Q(vehicle__vehicle_type__icontains=query)
        )

    if request.method == 'POST':
        vehicle_id = request.POST.get('vehicle')
        arrival_period_of_operation = request.POST.get('arrival_period_of_operation')
        departure_period_of_operation = request.POST.get('departure_period_of_operation')
        current_available_capacity = request.POST.get('current_available_capacity')

        transit_id = request.POST.get('transit_id')  # Get the ID of the transit schedule

        if transit_id:  # If the ID exists, update the existing entry
            transit_schedule = TransitSchedule.objects.get(id=transit_id)
            transit_schedule.vehicle_id = vehicle_id
            transit_schedule.arrival_period_of_operation = arrival_period_of_operation
            transit_schedule.departure_period_of_operation = departure_period_of_operation
            transit_schedule.current_available_capacity = current_available_capacity
            transit_schedule.save()
        else:  # If the ID does not exist, create a new entry
            TransitSchedule.objects.create(
                vehicle_id=vehicle_id,
                arrival_period_of_operation=arrival_period_of_operation,
                departure_period_of_operation=departure_period_of_operation,
                current_available_capacity=current_available_capacity
            )

        return redirect('transit')

    context = {
        'transit_schedules': transit_schedules,
        'vehicles': vehicles,
        'query': query,
    }
    return render(request, 'transit.html', context)
def transit_delete(request):
    if request.method == 'POST':
        transit_id = request.POST.get('delete')
        transit_schedule = get_object_or_404(TransitSchedule, id=transit_id)
        transit_schedule.delete()
    return redirect('transit')

def fooditem_view(request):
    fooditems = FoodItem.objects.all()

    query = request.GET.get('q')
    if query:
        fooditems = fooditems.filter(
            Q(name__icontains=query) |
            Q(food_group__icontains=query) |
            Q(expiration_date__icontains=query) |
            Q(item_size__icontains=query) |
            Q(associated_food_bank__street_address__icontains=query) |
            Q(donator__icontains=query)
        )

    if request.method == 'POST':
        name = request.POST.get('name')
        food_group = request.POST.get('food_group')
        expiration_date = request.POST.get('expiration_date')
        item_size = request.POST.get('item_size')
        associated_food_bank_id = request.POST.get('associated_food_bank')
        donator = request.POST.get('donator')

        expiration_date = request.POST.get('expiration_date')
        if expiration_date:  # Ensure expiration date is not empty
            expiration_date = datetime.strptime(expiration_date,
                                                '%Y-%m-%d').date()  # Parse the date string to a date object

        fooditem_id = request.POST.get('fooditem_id')  # Get the ID of the food item

        if fooditem_id:  # If the ID exists, update the existing entry
            fooditem = FoodItem.objects.get(id=fooditem_id)
            fooditem.name = name
            fooditem.food_group = food_group
            fooditem.expiration_date = expiration_date
            fooditem.item_size = item_size
            fooditem.associated_food_bank_id = associated_food_bank_id
            fooditem.donator = donator
            fooditem.save()
        else:  # If the ID does not exist, create a new entry
            FoodItem.objects.create(
                name=name,
                food_group=food_group,
                expiration_date=expiration_date,
                item_size=item_size,
                associated_food_bank_id=associated_food_bank_id,
                donator=donator
            )

        return redirect('fooditem')

    context = {
        'fooditems': fooditems,
        'query': query,
        'foodbanks': FoodBank.objects.all()
    }
    return render(request, 'fooditem.html', context)

def fooditem_delete(request):
    if request.method == 'POST':
        fooditem_id = request.POST.get('fooditem_id')
        fooditem = get_object_or_404(FoodItem, id=fooditem_id)
        fooditem.delete()
    return redirect('fooditem')
