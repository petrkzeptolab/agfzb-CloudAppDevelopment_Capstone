from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .restapis import *
import logging
import json
import random

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

def index(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


#Create a `login_request` view to handle sign in request
def login_request(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
    return redirect('djangoapp:index')

#Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def register(request):
    # If it is a GET request, just render the registration page
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")   
    context = {} 
    return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/ololorg_djangoserver-space/dealership-package/get-dealership.json"
        dealerships = get_dealers_from_cf(url)
        context = {} 
        context["dealerships"] = dealerships
        return render(request, 'djangoapp/index.html', context)
        
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # return HttpResponse(dealer_names)

def get_dealerships_by_state(request, state):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/ololorg_djangoserver-space/dealership-package/get-dealership.json"
        # Get dealers from the URL
        dealerships = get_dealers_by_state_cf(url, state)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.__str__() for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/ololorg_djangoserver-space/dealership-package/get-review.json"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context = {}
        context["dealer_id"] = dealer_id
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)
        # review_str = ' '.join([dealer.__str__() for review in reviews])
        # return HttpResponse(review_str)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "POST":
        if (request.user) :
            print(request.POST)
            url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/ololorg_djangoserver-space/dealership-package/post-review.json"
            review = dict()
            review["id"] = random.randint(1000, 999999)
            review["name"] = request.POST['name']
            review["dealership"] = dealer_id
            review["review"] = request.POST['content']
            review["purchase"] = request.POST.get('purchasecheck', False)
            review["time"] = datetime.utcnow().isoformat()
            
            json_payload = dict()
            json_payload["review"] = review

            result = post_request(url, json_payload)
            return redirect("djangoapp:dealer", dealer_id=dealer_id)
        else :
            return HttpResponse("not_logined")
    else :
        context = {}
        context["dealer_id"] = dealer_id
        context["cars"] = []
        for car in CarModel.objects.filter():
            context["cars"].append(car)
                
        return render(request, 'djangoapp/add_review.html', context)

