# Foodbank
Foodbank is a volunteer tracking system for food banks to help track volunteer’s availability, frequency of participation, coordinate transportation of volunteers to and from each food bank, and record which foods are most in need.

## Run Locally
After cloning the git repo, run the following commands to start the server:
- `python manage.py migrate`
- `python manage.py runserver`

You can use the `Setup DB` button on the main page after creating a user and logging in to add sample data to your local DB. This essentially just executes a bunch of SQL insert statements, so don't use it more than once and be careful using it after already adding data.