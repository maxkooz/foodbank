from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection

from .models import Volunteer, FoodBank, Task, Volunteer_Task, Vehicle, TransitSchedule, FoodItem, \
    RecipientOrganization, DistributedFoodItem, Donator, FoodGroup

import re
from datetime import datetime, timedelta
from collections import namedtuple

def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('foodbank:main_page')
        else:
            error_msg = 'Invalid credentials. Please try again.'
            return render(request, 'admin_login.html', {'error_msg': error_msg})
    return render(request, 'admin_login.html')
def home_view(request):
    error_msg = request.GET.get('error_msg')

    context = {
        'error_msg': error_msg
    }
    return render(request, 'home.html', context)

def login_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)

        return redirect(reverse('foodbank:limited_main_page'))
    else:
        error_msg = 'Login Failed. Please enter username and password or create new account.'
        return redirect(reverse('foodbank:home')+'?error_msg='+error_msg)
    
def logout_view(request):
    logout(request)
    return redirect(reverse('foodbank:limited_main_page'))

def sign_up_view(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    email = request.POST.get("email")

    user = User.objects.create_user(username, email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    login(request, user)

    return redirect(reverse('foodbank:limited_main_page'))

@login_required(login_url='/login/')
def limited_main_page_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse('foodbank:home'))

    return render(request, 'limited_main_page.html')


def main_page_view(request):
    if not request.user.is_authenticated:
        return redirect(reverse('foodbank:home'))

    return render(request, 'main_page.html')

# from Django documentation
def namedtuplefetchall(cursor):
    """
    Return all rows from a cursor as a namedtuple.
    Assume the column names are unique.
    """
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def execute_raw_sql(query, fetch=True):
    with connection.cursor() as cursor:
        cursor.execute(query)
        res = namedtuplefetchall(cursor) if fetch else None
    
    return res

class VolunteerView(LoginRequiredMixin, generic.ListView):
    login_url = "/login/"
    redirect_field_name = ""
    model = Volunteer
    template_name='volunteer.html'
    context_object_name='volunteers'
    # phoneNumberRegex = re.compile("^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$")
    # emailRegex = re.compile("[^@]+@[^@]+\.[^@]+")

    def get_queryset(self):
        return Volunteer.objects.all()
    
    def get(self, req):
        error_msg = req.GET.get('error_msg') if 'error_msg' in req.GET else None
        volunteers = self.get_queryset()
        query = req.GET.get('q')
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

        # data summary queries
        # group volunteers by city
        res = execute_raw_sql("SELECT city, COUNT(id) AS NumVolunteers FROM foodbank_volunteer GROUP BY city;")

        context = {
            self.context_object_name: volunteers,
            'vol_count_by_city': res,
            'error_msg': error_msg,
        }

        return render(req, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        error_msgs = []

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        home_state = request.POST.get('home_state')
        zip_code = request.POST.get('zip_code')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        # Check that at least one field is not empty
        if validateTextFields([first_name, last_name, street_address, city, home_state, zip_code, phone_number, email], error_msgs):            
            if 'add' in request.POST:
            
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

                for field in Volunteer._meta.get_fields():
                    name = field.name
                    if name != 'id' and name in request.POST and request.POST.get(name) != "":
                        newval = request.POST.get(name)
                        print(name, newval)
                        
                        volunteer.__setattr__(name, newval)
                
                volunteer.save()
            elif 'delete' in request.POST:
                volunteer_id = request.POST.get('volunteer_id')

                try:
                    Volunteer.objects.get(id=volunteer_id).delete()
                except Volunteer.DoesNotExist:
                    error_msg = 'Error when deleting Volunteer ' + str(volunteer_id) + ': volunteer does not exist'
                    return redirect(reverse("foodbank:volunteers")+'?error_msg='+error_msg)

        else:
            return redirect(reverse("foodbank:volunteers")+'?error_msg='+'\r\n'.join(error_msgs))



        return redirect(reverse("foodbank:volunteers"))


class FoodBankView(LoginRequiredMixin, generic.ListView):
    login_url = "/login/"
    redirect_field_name = ""
    model=FoodBank
    context_object_name='foodbanks'
    template_name='foodbank.html'

    def get_queryset(self):
        return FoodBank.objects.all()
    
    def get(self, req):
        error_msg = req.GET.get('error_msg') if 'error_msg' in req.GET else None
        foodbanks = self.get_queryset()
        potential_managers = Volunteer.objects.all()

        query = req.GET.get('q')
        if query:
            foodbanks = foodbanks.filter(
                Q(street_address__icontains=query) |
                Q(city__icontains=query) |
                Q(home_state__icontains=query) |
                Q(zip_code_icontains=query) |
                Q(phone_number__icontains=query) |
                Q(email__icontains=query)
            )

        # data summary queries
        # group food banks by city
        res = execute_raw_sql("SELECT city, COUNT(id) AS NumFoodBanks FROM foodbank_foodbank GROUP BY city;")

        context = {
            self.context_object_name: foodbanks,
            'food_bank_count_by_city': res,
            'potential_managers': potential_managers,
            'error_msg': error_msg,
        }

        return render(req, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        error_msgs = []

        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        home_state = request.POST.get('home_state')
        zip_code = request.POST.get('zip_code')
        manager = request.POST.get('manager')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        if validateTextFields([street_address, city, home_state, zip_code, phone_number, email], error_msgs) and self.validateForeignKey(manager, error_msgs):
            if 'add' in request.POST:
                FoodBank.objects.create(
                    street_address=street_address,
                    city=city,
                    home_state=home_state,
                    zip_code=zip_code,
                    manager=Volunteer.objects.get(pk=manager),
                    phone_number=phone_number,
                    email=email
                )
            elif 'edit' in request.POST:
                foodbank_id = request.POST.get('foodbank_id')
                foodbank = FoodBank.objects.get(id=foodbank_id)

                for field in FoodBank._meta.get_fields():
                    name = field.name
                    if name != 'id' and name in request.POST and request.POST.get(name) != "":
                        newval = request.POST.get(name)
                        if name == 'manager':
                            newval = Volunteer.objects.get(id=newval)
                        
                        foodbank.__setattr__(name, newval)

                # Update other fields for editing
                foodbank.save()
            elif 'delete' in request.POST:
                foodbank_id = request.POST.get('foodbank_id')

                try:
                    FoodBank.objects.get(id=foodbank_id).delete()
                except FoodBank.DoesNotExist:
                    error_msg = 'Error when deleting Food Bank ' + str(foodbank_id) + ': food bank does not exist'
                    return redirect(reverse("foodbank:foodbanks")+'?error_msg='+error_msg)
            
            return redirect(reverse('foodbank:foodbanks'))
        else:
            return redirect(reverse("foodbank:foodbanks")+'?error_msg='+'\r\n'.join(error_msgs))
    
    def validateForeignKey(self, fk, error_msgs):
        if Volunteer.objects.filter(pk=fk).exists():
            return True
        
        error_msgs.append('Foreign key value must correspond to an entity that exists within foreign table')
        return False

def validateTextFields(fields, error_msgs):
    for field in fields:
        if field == "":
            error_msgs.append('No text fields can be empty')
            return False
        
    return True

def validateIntFields(fields, error_msgs):
    for field in fields:
        try:
            tmp = int(field)
        except ValueError:
            error_msgs.append('Integer fields must have integer values')
            return False
        
    return True

def validateDateTimeFields(fields, error_msgs):
    for field in fields:
        if field == "":
            error_msgs.append('No datetime fields can be empty')
            return False
        
    return True


class TaskView(LoginRequiredMixin, generic.ListView):
    login_url = "/login/"
    redirect_field_name = ""
    model=Task
    foreign_model = FoodBank
    context_object_name='tasks'
    foreign_context_name = 'foodbanks'
    template_name='task.html'
    vols_per_task_exists = False

    textFields = ['description']
    intFields = ['min_volunteers', 'max_volunteers']
    datetimeFields = ['start_date_time', 'end_date_time']
    foreignKeyFields = ['associated_food_bank']

    def get_queryset(self):
        return self.model.objects.all()
    
    def get_foreign_queryset(self):
        return self.foreign_model.objects.all()
    
    def get(self, req):
        error_msg = req.GET.get('error_msg') if 'error_msg' in req.GET else None
        entities = self.get_queryset()
        foreign_entities = self.get_foreign_queryset()

        query = req.GET.get('q')
        if query:
            entities = entities.filter(
                Q(description__icontains=query) |
                Q(start_date_time__icontains=query) |
                Q(end_date_time__icontains=query)
            )

        # data summary queries
        # number of tasks per food bank
        tasks_per_fb = execute_raw_sql("SELECT associated_food_bank_id, COUNT(id) AS NumTasks FROM foodbank_task GROUP BY associated_food_bank_id;")

        # create VolsPerTask view in DB
        if not self.vols_per_task_exists:
            _ = execute_raw_sql("DROP VIEW IF EXISTS foodbank_VolsPerTask;", fetch=False)
            _ = execute_raw_sql("CREATE VIEW foodbank_VolsPerTask AS SELECT task_id, SUM(CurVolsSignedUp) as CurVolsSignedUp FROM (SELECT vt.task_id, COUNT(vt.volunteer_id) AS CurVolsSignedUp FROM foodbank_volunteer_task vt GROUP BY vt.task_id UNION SELECT t.id as task_id, 0 as CurVolsSignedUp FROM foodbank_task t) AS T GROUP BY task_id;", fetch=False)
            self.vols_per_task_exists = True
        
        # get number of volunteers signed up for each task
        cur_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        vols_per_task = execute_raw_sql("SELECT vpt.task_id AS t_id, t.description AS t_descr, t.start_date_time AS t_start, t.end_date_time AS t_end, fb.id AS fb_id, t.min_volunteers AS t_min, t.max_volunteers AS t_max, vpt.CurVolsSignedUp as t_cur "+\
                              "FROM foodbank_VolsPerTask vpt JOIN foodbank_task t ON vpt.task_id=t.id JOIN foodbank_foodbank fb ON t.associated_food_bank_id=fb.id "+\
                                f"WHERE vpt.CurVolsSignedUp < t.max_volunteers AND t.start_date_time > '{cur_datetime}';")

        context = {
            self.context_object_name: entities,
            self.foreign_context_name: foreign_entities,
            'tasks_per_fb': tasks_per_fb,
            'vols_per_task': vols_per_task,
            'volunteers': Volunteer.objects.all(),
            'query': query,
            'error_msg': error_msg,
        }

        return render(req, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        if 'signup' in request.POST:
            vol_id = request.POST.get('vol_signing_up')
            vol = Volunteer.objects.get(id=vol_id)
            task_id = request.POST.get('task_id')
            task = Task.objects.get(id=task_id)

            Volunteer_Task.objects.create(volunteer=vol, task=task)

            return redirect(reverse('foodbank:'+self.context_object_name))
        
        field_name_to_newval = {}
        error_msgs = []

        for field in self.model._meta.get_fields():
            name = field.name
            if name in request.POST and request.POST.get(name) != "":
                field_name_to_newval[name] = request.POST.get(name)

        if validateTextFields([field_name_to_newval[f] for f in self.textFields], error_msgs) \
            and validateIntFields([field_name_to_newval[f] for f in self.intFields], error_msgs) \
            and validateDateTimeFields([field_name_to_newval[f] for f in self.datetimeFields], error_msgs) \
            and self.validateForeignKey([field_name_to_newval[f] for f in self.foreignKeyFields], error_msgs):
            if 'add' in request.POST:
                new_entity = self.model.objects.create()

                for field_name, val in field_name_to_newval.items():
                    if field_name != 'id':
                        if field_name in self.foreignKeyFields:
                            val = self.foreign_model.objects.get(id=val)
                        if field_name in self.datetimeFields:
                            print(val, print(type(val)))
                        
                        new_entity.__setattr__(field_name, val)

                new_entity.save()

            elif 'edit' in request.POST:
                entity_id = request.POST.get(self.model._meta.model_name + '_id')
                entity = self.model.objects.get(id=entity_id)

                for field_name, val in field_name_to_newval.items():
                    if field_name != 'id':
                        if field_name in self.foreignKeyFields:
                            val = self.foreign_model.objects.get(id=val)
                        
                        entity.__setattr__(field_name, val)

                entity.save()
            elif 'delete' in request.POST:
                entity_id = request.POST.get(self.model._meta.model_name + '_id')

                try:
                    self.model.objects.get(id=entity_id).delete()
                except self.model.DoesNotExist:
                    error_msg = 'Error when deleting ' + self.model._meta + ' ' + str(entity_id) + ': entity does not exist'
                    return redirect(reverse("foodbank:"+self.context_object_name)+'?error_msg='+error_msg)
            
            return redirect(reverse('foodbank:'+self.context_object_name))
        else:
            return redirect(reverse("foodbank:"+self.context_object_name)+'?error_msg='+'\r\n'.join(error_msgs))
    
    def validateForeignKey(self, fks, error_msgs):
        if self.foreign_model.objects.filter(pk=fks[0]).exists():
            return True
        error_msgs.append('Foreign key value must correspond to an entity that exists within foreign table')
        return False


@login_required(login_url='/login/')
def volunteer_task_view(request):
    shifts = Volunteer_Task.objects.select_related('volunteer', 'task', 'task__associated_food_bank').all()
    volunteers = Volunteer.objects.all()
    tasks = Task.objects.all()

    query = request.GET.get('q')
    if query:
        shifts = shifts.filter(
            Q(volunteer__first_name__icontains=query) |  # Search by volunteer first name
            Q(volunteer__last_name__icontains=query) |   # Search by volunteer last name
            Q(task__description__icontains=query) | # Search by task description
            Q(task__associated_food_bank__city__icontains=query)
        )

    if request.method == 'POST':
        volunteer_id = request.POST.get('volunteer')
        task_id = request.POST.get('task')

        shift_id = request.POST.get('shift_id')  # Get the ID of the shift

        if shift_id:  # If the ID exists, update the existing entry
            shift = Volunteer_Task.objects.get(id=shift_id)
            shift.volunteer_id = volunteer_id
            shift.task_id = task_id
            shift.save()
        else:  # If the ID does not exist, create a new entry
            Volunteer_Task.objects.create(
                volunteer_id=volunteer_id,
                task_id=task_id
            )

        return redirect(reverse('foodbank:volunteer_tasks'))

    context = {
        'shifts': shifts,
        'volunteers': volunteers,
        'tasks': tasks,
        'query': query,
    }
    return render(request, 'volunteer_task.html', context)

@login_required(login_url='/login/')
def volunteer_task_delete(request):
    if request.method == 'POST':
        shift_id = request.POST.get('shift_id')
        shift = get_object_or_404(Volunteer_Task, id=shift_id)
        shift.delete()
    return redirect(reverse('foodbank:volunteer_tasks'))

@login_required(login_url='/login/')
def volunteer_task_delete(request):
    if request.method == 'POST':
        shift_id = request.POST.get('shift_id')
        shift = get_object_or_404(Volunteer_Task, id=shift_id)
        shift.delete()
    return redirect(reverse('foodbank:volunteer_tasks'))

class VehcileView(LoginRequiredMixin, generic.ListView):
    login_url = "/login/"
    redirect_field_name = ""
    model=Vehicle
    foreign_model = Volunteer
    context_object_name='vehicles'
    foreign_context_name = 'volunteers'
    template_name='vehicle.html'

    textFields = ['vehicle_type']
    intFields = ['total_passenger_capacity']
    foreignKeyFields = ['driver_volunteer']

    def get_queryset(self):
        return self.model.objects.all()
    
    def get_foreign_queryset(self):
        return self.foreign_model.objects.all()
    
    def get(self, req):
        error_msg = req.GET.get('error_msg') if 'error_msg' in req.GET else None
        entities = self.get_queryset()
        foreign_entities = self.get_foreign_queryset()

        query = req.GET.get('q')
        if query:
            entities = entities.filter(
                Q(vehcile_type__icontains=query)
            )

        # data summary queries
        vehicles_per_type = execute_raw_sql("SELECT vehicle_type, COUNT(id) as num_vehicles, SUM(total_passenger_capacity) as cum_capacity FROM foodbank_vehicle GROUP BY vehicle_type;")
  
        context = {
            self.context_object_name: entities,
            self.foreign_context_name: foreign_entities,
            'vehicles_per_type': vehicles_per_type,
            'query': query,
            'error_msg': error_msg,
        }

        return render(req, self.template_name, context)
    
    def post(self, request, *args, **kwargs):        
        field_name_to_newval = {}
        error_msgs = []

        for field in self.model._meta.get_fields():
            name = field.name
            if name in request.POST and request.POST.get(name) != "":
                field_name_to_newval[name] = request.POST.get(name)

        if validateTextFields([field_name_to_newval[f] for f in self.textFields], error_msgs) \
            and validateIntFields([field_name_to_newval[f] for f in self.intFields], error_msgs) \
            and self.validateForeignKey([field_name_to_newval[f] for f in self.foreignKeyFields], error_msgs):
            if 'add' in request.POST:
                new_entity = self.model.objects.create()

                for field_name, val in field_name_to_newval.items():
                    if field_name != 'id':
                        if field_name in self.foreignKeyFields:
                            val = self.foreign_model.objects.get(id=val)
                        
                        new_entity.__setattr__(field_name, val)

                new_entity.save()

            elif 'edit' in request.POST:
                entity_id = request.POST.get(self.model._meta.model_name + '_id')
                entity = self.model.objects.get(id=entity_id)

                for field_name, val in field_name_to_newval.items():
                    if field_name != 'id':
                        if field_name in self.foreignKeyFields:
                            val = self.foreign_model.objects.get(id=val)
                        
                        entity.__setattr__(field_name, val)

                entity.save()
            elif 'delete' in request.POST:
                entity_id = request.POST.get(self.model._meta.model_name + '_id')

                try:
                    self.model.objects.get(id=entity_id).delete()
                except self.model.DoesNotExist:
                    error_msg = 'Error when deleting ' + self.model._meta + ' ' + str(entity_id) + ': entity does not exist'
                    return redirect(reverse("foodbank:"+self.context_object_name)+'?error_msg='+error_msg)
            
            return redirect(reverse('foodbank:'+self.context_object_name))
        else:
            return redirect(reverse("foodbank:"+self.context_object_name)+'?error_msg='+'\r\n'.join(error_msgs))
    
    def validateForeignKey(self, fks, error_msgs):
        if self.foreign_model.objects.filter(pk=fks[0]).exists():
            return True
        error_msgs.append('Foreign key value must correspond to an entity that exists within foreign table')
        return False

class TransitView(LoginRequiredMixin, generic.ListView):
    login_url = "/login/"
    redirect_field_name = ""
    model=TransitSchedule
    foreign_model = Vehicle
    context_object_name='transits'
    foreign_context_name = 'vehicles'
    template_name='transit.html'

    datetimeFields = ['arrival_date_time', 'departure_date_time']
    intFields = ['current_available_capacity']
    foreignKeyFields = ['vehicle']

    def get_queryset(self):
        return self.model.objects.all()
    
    def get_foreign_queryset(self):
        return self.foreign_model.objects.all()
    
    def get(self, req):
        error_msg = req.GET.get('error_msg') if 'error_msg' in req.GET else None
        entities = self.get_queryset()
        foreign_entities = self.get_foreign_queryset()

        query = req.GET.get('q')
        # if query:
        #     entities = entities.filter(
        #         Q(vehcile_type__icontains=query)
        #     )

        # data summary queries
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        today = today.strftime("%Y-%m-%d")
        tomorrow = tomorrow.strftime("%Y-%m-%d")
        print(today, tomorrow)
        transits_today = execute_raw_sql(f"SELECT ts.id AS ts_id, ts.current_available_capacity, vo.first_name, vo.last_name, ve.vehicle_type FROM foodbank_transitschedule ts JOIN foodbank_vehicle ve ON ts.vehicle_id=ve.id JOIN foodbank_volunteer vo ON vo.id=ve.driver_volunteer_id WHERE ts.current_available_capacity > 0 AND ts.arrival_date_time BETWEEN '{today}' AND '{tomorrow}';")
        

        context = {
            self.context_object_name: entities,
            self.foreign_context_name: foreign_entities,
            'transits_today': transits_today,
            'query': query,
            'error_msg': error_msg,
        }

        return render(req, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # current just decrements available capacity on join   
        if 'join' in request.POST:
            transit_id = request.POST.get('transit_id')
            transit = self.model.objects.get(id=transit_id)
            transit.current_available_capacity -= 1
            transit.save()

            return redirect(reverse("foodbank:"+self.context_object_name))

        field_name_to_newval = {}
        error_msgs = []

        for field in self.model._meta.get_fields():
            name = field.name
            if name in request.POST and request.POST.get(name) != "":
                field_name_to_newval[name] = request.POST.get(name)

        if validateDateTimeFields([field_name_to_newval[f] for f in self.datetimeFields], error_msgs) \
            and validateIntFields([field_name_to_newval[f] for f in self.intFields], error_msgs) \
            and self.validateForeignKey([field_name_to_newval[f] for f in self.foreignKeyFields], error_msgs):
            if 'add' in request.POST:
                new_entity = self.model.objects.create()

                for field_name, val in field_name_to_newval.items():
                    if field_name != 'id':
                        if field_name in self.foreignKeyFields:
                            val = self.foreign_model.objects.get(id=val)
                        
                        new_entity.__setattr__(field_name, val)

                new_entity.save()

            elif 'edit' in request.POST:
                entity_id = request.POST.get('transit_id')
                entity = self.model.objects.get(id=entity_id)

                for field_name, val in field_name_to_newval.items():
                    if field_name != 'id':
                        if field_name in self.foreignKeyFields:
                            val = self.foreign_model.objects.get(id=val)
                        
                        entity.__setattr__(field_name, val)

                entity.save()
            elif 'delete' in request.POST:
                entity_id = request.POST.get('transit_id')

                try:
                    self.model.objects.get(id=entity_id).delete()
                except self.model.DoesNotExist:
                    error_msg = 'Error when deleting ' + self.model._meta + ' ' + str(entity_id) + ': entity does not exist'
                    return redirect(reverse("foodbank:"+self.context_object_name)+'?error_msg='+error_msg)
            
            return redirect(reverse('foodbank:'+self.context_object_name))
        else:
            return redirect(reverse("foodbank:"+self.context_object_name)+'?error_msg='+'\r\n'.join(error_msgs))
    
    def validateForeignKey(self, fks, error_msgs):
        if self.foreign_model.objects.filter(pk=fks[0]).exists():
            return True
        error_msgs.append('Foreign key value must correspond to an entity that exists within foreign table')
        return False

@login_required(login_url='/login/')
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

        return redirect(reverse('foodbank:transits'))

    context = {
        'transit_schedules': transit_schedules,
        'vehicles': vehicles,
        'query': query,
    }
    return render(request, 'transit.html', context)

@login_required(login_url='/login/')
def transit_delete(request):
    if request.method == 'POST':
        transit_id = request.POST.get('delete')
        transit_schedule = get_object_or_404(TransitSchedule, id=transit_id)
        transit_schedule.delete()
    return redirect(reverse('foodbank:transits'))

@login_required(login_url='/login/')
def transit_capacity(request):
    query = request.GET.get('q')
    transit_schedules = TransitSchedule.objects.all()
    if query:
        transit_schedules = transit_schedules.filter(Q(current_available_capacity__gte=query)) #change gte value to user's search input

    # if request.method == 'POST':
    #     vehicle_id = request.POST.get('vehicle_id')
    #     vehicle = Vehicle.objects.get(id=vehicle_id)
    #     vehicle.arrival_period_of_operation = request.POST.get('arrival_period_of_operation')
    #     vehicle.departure_period_of_operation = request.POST.get('departure_period_of_operation')
    #     vehicle.current_available_capacity = request.POST.get('current_available_capacity')
    #     vehicle.save()
    #return redirect('transit')
    return render(request, 'transit.html', {'transit_schedules': transit_schedules})

@login_required(login_url='/login/')
def fooditem_view(request):
    fooditems = FoodItem.objects.all()
    donators = Donator.objects.all()
    food_groups = FoodGroup.objects.all()

    query = request.GET.get('q')
    if query:
        fooditems = fooditems.filter(
            Q(name__icontains=query) |
            Q(food_group__name__icontains=query) |
            Q(expiration_date__icontains=query) |
            Q(item_size__icontains=query) |
            Q(associated_food_bank__street_address__icontains=query) |
            Q(donator__first_name__icontains=query) |
            Q(donator__last_name__icontains=query)
        )

    if request.method == 'POST':
        name = request.POST.get('name')
        food_group_id = request.POST.get('food_group')
        expiration_date = request.POST.get('expiration_date')
        item_size = request.POST.get('item_size')
        associated_food_bank_id = request.POST.get('associated_food_bank')
        donator_id = request.POST.get('donator')

        expiration_date = datetime.strptime(expiration_date, '%Y-%m-%d').date() if expiration_date else None

        fooditem_id = request.POST.get('fooditem_id')

        if fooditem_id:
            fooditem = FoodItem.objects.get(id=fooditem_id)
            fooditem.name = name
            fooditem.food_group_id = food_group_id
            fooditem.expiration_date = expiration_date
            fooditem.item_size = item_size
            fooditem.associated_food_bank_id = associated_food_bank_id
            fooditem.donator_id = donator_id
            fooditem.save()
        else:
            FoodItem.objects.create(
                name=name,
                food_group_id=food_group_id,
                expiration_date=expiration_date,
                item_size=item_size,
                associated_food_bank_id=associated_food_bank_id,
                donator_id=donator_id
            )

        return redirect(reverse('foodbank:fooditems'))

    context = {
        'fooditems': fooditems,
        'query': query,
        'foodbanks': FoodBank.objects.all(),
        'donators': donators,
        'food_groups': food_groups,
    }
    return render(request, 'fooditem.html', context)

@login_required(login_url='/login/')
def fooditem_delete(request):
    if request.method == 'POST':
        fooditem_id = request.POST.get('fooditem_id')
        fooditem = get_object_or_404(FoodItem, id=fooditem_id)
        fooditem.delete()
    return redirect(reverse('foodbank:fooditems'))

@login_required(login_url='/login/')
def recipient_organization_view(request):
    recipient_organizations = RecipientOrganization.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        home_state = request.POST.get('home_state')
        zip_code = request.POST.get('zip_code')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        recipient_organization_id = request.POST.get('recipient_organization_id')
        if recipient_organization_id:
            recipient_organization = RecipientOrganization.objects.get(id=recipient_organization_id)
            recipient_organization.name = name
            recipient_organization.street_address = street_address
            recipient_organization.city = city
            recipient_organization.home_state = home_state
            recipient_organization.zip_code = zip_code
            recipient_organization.phone_number = phone_number
            recipient_organization.email = email
            recipient_organization.save()
        else:
            RecipientOrganization.objects.create(
                name=name,
                street_address=street_address,
                city=city,
                home_state=home_state,
                zip_code=zip_code,
                phone_number=phone_number,
                email=email
            )

        return redirect(reverse('foodbank:recipient_organizations'))

    context = {
        'recipient_organizations': recipient_organizations,
    }
    return render(request, 'recipient_organization.html', context)

@login_required(login_url='/login/')
def recipient_organization_delete(request):
    if request.method == 'POST':
        recipient_organization_id = request.POST.get('recipient_organization_id')
        recipient_organization = get_object_or_404(RecipientOrganization, id=recipient_organization_id)
        recipient_organization.delete()
    return redirect(reverse('foodbank:recipient_organizations'))

@login_required(login_url='/login/')
def distributed_food_item_view(request):
    items = DistributedFoodItem.objects.all()
    food_items = FoodItem.objects.all()
    recipient_organizations = RecipientOrganization.objects.all()

    if request.method == 'POST':
        if 'add' in request.POST:
            food_item_id = request.POST.get('food_item')
            recipient_org_id = request.POST.get('recipient_organization')

            DistributedFoodItem.objects.create(
                food_item_id=food_item_id,
                recipient_org_id=recipient_org_id
            )
        elif 'save' in request.POST:
            item_id = request.POST.get('item_id')
            item = DistributedFoodItem.objects.get(id=item_id)
            food_item_id = request.POST.get('food_item')
            recipient_org_id = request.POST.get('recipient_organization')
            item.food_item_id = food_item_id
            item.recipient_org_id = recipient_org_id
            item.save()

        return redirect(reverse('foodbank:distributed_food_items'))

    context = {
        'distributed_food_items': items,
        'food_items': food_items,
        'recipient_organizations': recipient_organizations,
    }
    return render(request, 'distributed_food_item.html', context)

@login_required(login_url='/login/')
def distributed_food_item_delete(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = get_object_or_404(DistributedFoodItem, id=item_id)
        item.delete()
    return redirect(reverse('foodbank:distributed_food_items'))

@login_required(login_url='/login/')
def donator_view(request):
    donators = Donator.objects.all().prefetch_related('fooditem_set')

    if request.method == 'POST':
        donator_id = request.POST.get('donator_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')

        if donator_id:
            donator = Donator.objects.get(id=donator_id)
            donator.first_name = first_name
            donator.last_name = last_name
            donator.phone_number = phone_number
            donator.email = email
            donator.save()
        else:
            Donator.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email
            )

        return redirect(reverse('foodbank:donators'))

    context = {
        'donators': donators,
    }
    return render(request, 'donator.html', context)
def donator_delete(request):
    if request.method == 'POST':
        donator_id = request.POST.get('donator_id')
        donator = get_object_or_404(Donator, id=donator_id)
        donator.delete()
    return redirect(reverse('foodbank:donators'))

@login_required(login_url='/login/')
def foodgroup_view(request):
    foodgroups = FoodGroup.objects.all()

    if request.method == 'POST':
        foodgroup_id = request.POST.get('foodgroup_id')
        name = request.POST.get('name')

        if foodgroup_id:
            foodgroup = FoodGroup.objects.get(id=foodgroup_id)
            foodgroup.name = name
            foodgroup.save()
        else:
            FoodGroup.objects.create(
                name=name
            )

        return redirect(reverse('foodbank:foodgroups'))

    context = {
        'foodgroups': foodgroups,
    }
    return render(request, 'foodgroup.html', context)

@login_required(login_url='/login/')
def foodgroup_delete(request):
    if request.method == 'POST':
        foodgroup_id = request.POST.get('foodgroup_id')
        foodgroup = get_object_or_404(FoodGroup, id=foodgroup_id)
        foodgroup.delete()
    return redirect(reverse('foodbank:foodgroups'))
