from django.db import models
from django.utils.timezone import now
from django.core import serializers 
import uuid
import json

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=20, default='undefined')
    # - Name
    description = models.TextField(null=True)
    # - Description
    def __str__(self):
    # - __str__ method to print a car make object
        return self.name + ": " + self.description


class CarModel(models.Model):
    make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)  
    # - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
    name = models.CharField(null=False, max_length=40, default='undefined')
    # - Name
    id = models.IntegerField(default=1,primary_key=True)        
    # - Dealer id, used to refer a dealer created in cloudant database
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    COUPE = 'Coupe'
    SPORTS = 'Sports'
    HATCHBACK = 'Hatchback'
    CONVERTIBLE = 'Convertible'
    MINIVAN = 'Minivan'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (COUPE, 'Coupe'),
        (SPORTS, 'Sports'),
        (HATCHBACK, 'Hatchback'),
        (CONVERTIBLE, 'Convertible'),
        (MINIVAN, 'Minivan'),   
    ]
    type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=COUPE
    )
    # - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
    year = models.DateTimeField('date designed')
    def __str__(self):
        return self.type
    # - __str__ method to print a car make object


class CarDealer:


    def __init__(self, address, city, full_name, id, lat, long, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer full name
        self.full_name=full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long

        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


class DealerReview:

    def __init__(self, dealership, name, purchase, review):
        # Required attributes
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        # Optional attributes
        self.purchase_date = ""
        self.purchase_make = ""
        self.purchase_model = ""
        self.purchase_year = ""
        self.sentiment = ""
        self.id = ""

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)

class ReviewPost:

    def __init__(self, dealership, name, purchase, review):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = ""
        self.car_make = ""
        self.car_model = ""
        self.car_year = ""

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)