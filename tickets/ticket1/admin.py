from django.contrib import admin
from ticket1.models import Route ,\
                            City
class CityAdmin(admin.ModelAdmin):
    list_display = ('City_Name',  'City_Country')
    search_fields = ('City_Name', 'City_Country')
    list_filter = ('City_Name',)
    # filter_horizontal = ('City_Name',)
    # ordering = ('City_Name',)
    # fields = ('City_Name', 'City_Country',)
    #raw_id_fields = ('City_ID',)
                            
                            
admin.site.register(Route)
admin.site.register(City,CityAdmin)
