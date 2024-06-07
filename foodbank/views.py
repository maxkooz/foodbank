from django.shortcuts import render, redirect
# Create your views here.iuhiuhi
from django.shortcuts import render
from .models import Volunteer
def home_view(request):
    return render(request, 'home.html')

def volunteer_view(request):
    volunteers = Volunteer.objects.all()

    query = request.GET.get('q')
    if query:
        volunteers = volunteers.filter(first_name__icontains=query)

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