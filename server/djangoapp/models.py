from django.db import models
from django.utils.timezone import now

 
# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return "{Name: " + self.name + "," + \
               "Description: " + self.description + "}"

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    TYPE_CHOICES = [
        ("sedan", 'SEDAN'),
        ("sub", 'SUV'),
        ("wagon", 'WAGON'),
        ("other", 'OTHER'),
    ]

    carMake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    dealerid = models.IntegerField(default=0)
    year = models.DateField(default=now)
    modelType = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default="other"
    )
    
    def __str__(self):
        return "{carMake: " + str(self.carMake) + "," + \
               "name: " + self.name + \
               "dealerid: " + str(self.dealerid) + \
               "year: " + str(self.year) + \
               "modelType: " + self.modelType + \
               "}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "{Dealer name: " + self.full_name+"}"


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, car_make, car_model, car_year, dealership, name, purchase, purchase_date, review, time, sentiment):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.time = time
        self.sentiment = sentiment

    def __str__(self):
        return "{Dealer name: " + self.name + " sentiment:" + str(self.sentiment) + " review:" + self.review + "}"