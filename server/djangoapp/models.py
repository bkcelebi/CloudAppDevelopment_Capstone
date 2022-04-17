from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

class CarMake(models.Model):
    make_name = models.CharField(max_length=64)
    make_description = models.CharField(null=True, max_length=64)

    def __str__(self):
        return "Name " + self.make_name + "," \
               "Description " + self.make_description


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    model_name = models.CharField(null=False, max_length=64)
    model_type = models.CharField(
        null=False,
        max_length=20,
        choices=[
            ('sedan', 'SEDAN'),
            ('suv', 'Sports Utility Vehicle'),
            ('coupe', 'Coupe'),
            ('wagon', 'Wagon'),
            ('convertible', 'Convertible'),
        ],
        default='sedan'
    ),
    model_year = models.DateField()

    def __str__(self):
        return f"{self.model_name} ({self.model_type}) - {self.model_year}"


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
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:

    def __init__(self, dealership, reviewer_name, review, purchase, purchase_date, car_make, car_model, car_year, sentiment, id):
        # Dealership
        self.dealership = dealership
        # Dealer name
        self.reviewer_name = reviewer_name
        # Review text
        self.review = review
        # Purchase info
        self.purchase = purchase
        self.purchase_date = purchase_date
        # Car info
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        # Review sentiment
        self.sentiment = sentiment
        # Review id
        self.id = id

    def __str__(self):
        return f"Review on dealer {self.dealership}: {self.review} ({self.sentiment})"
