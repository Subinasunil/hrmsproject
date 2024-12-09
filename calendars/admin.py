from django.contrib import admin
from .models import weekend_calendar,assign_weekend,holiday,holiday_calendar,assign_holiday

@admin.register(weekend_calendar)
class CountryAdmin(admin.ModelAdmin):
    pass
@admin.register(assign_weekend)
class CountryAdmin(admin.ModelAdmin):
    pass
@admin.register(holiday)
class CountryAdmin(admin.ModelAdmin):
    pass
@admin.register(holiday_calendar)
class CountryAdmin(admin.ModelAdmin):
    pass
@admin.register(assign_holiday)
class CountryAdmin(admin.ModelAdmin):
    pass