from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.iuhiuhi
from django.shortcuts import render
from .models import Volunteer, FoodBank
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