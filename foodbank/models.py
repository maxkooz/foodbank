from django.db import models

class Volunteer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    home_state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

class FoodBank(models.Model):
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=50)
    manager = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True, blank=True)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

class Task(models.Model):
    description = models.CharField(max_length=255)
    start_date_time = models.DateTimeField()
    end_date_time = models.DateTimeField()
    associated_food_bank = models.ForeignKey(FoodBank, on_delete=models.CASCADE, null=True, blank=True)
    min_volunteers = models.IntegerField()
    max_volunteers = models.IntegerField()

class IndividualShift(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True, blank=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)

class Vehicle(models.Model):
    driver_volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, null=True, blank=True)
    vehicle_type = models.CharField(max_length=255)
    total_passenger_capacity = models.IntegerField()

class TransitSchedule(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True, blank=True)
    arrival_period_of_operation = models.DateTimeField()
    departure_period_of_operation = models.DateTimeField()
    current_available_capacity = models.IntegerField()

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    food_group = models.CharField(max_length=50)
    expiration_date = models.DateField()
    item_size = models.CharField(max_length=255)
    associated_food_bank = models.ForeignKey(FoodBank, on_delete=models.CASCADE, null=True, blank=True)
    donator = models.CharField(max_length=255)

class DistributedFoodItem(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE, null=True, blank=True)
    recipient_org = models.ForeignKey('RecipientOrganization', on_delete=models.CASCADE, null=True, blank=True)

class RecipientOrganization(models.Model):
    name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    home_state = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
