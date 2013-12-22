from siteCoGM.apps.userdata.models import Userdata
from django.contrib import admin
 
 
class UserdataAdmin(admin.ModelAdmin):
    # list_display = ('name')
    # search_fields = ('name')
    # ordering = ('name',)
    pass
admin.site.register(Userdata, UserdataAdmin)
