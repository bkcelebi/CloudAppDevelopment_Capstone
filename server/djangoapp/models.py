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


# <HINT> Create a plain Python class `DealerReview` to hold review data
