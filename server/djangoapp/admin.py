from django.contrib import admin
from .models import CarModel, CarMake
# from .models import related models


# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'model_type')
    search_fields = ['model_name']

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ['make_name', 'make_description']
    list_filter = ['make_name']
    search_fields = ['make_name', 'make_description']

# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)
