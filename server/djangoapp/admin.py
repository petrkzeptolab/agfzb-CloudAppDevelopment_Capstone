from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel


# Register your models here.

# CarModelInline clas
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5 

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    model = CarModel
    list_display = ('name', 'modelType', 'dealerid')

# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    model = CarMake
    list_display = ('name', 'description')
    inlines = [CarModelInline]

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)

# Register models here
