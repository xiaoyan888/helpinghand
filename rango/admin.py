from django.contrib import admin
from rango.models import Category, Page, UserProfile

# Add in this class to customized the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class PageAdmin(admin.ModelAdmin):
   list_display = ('title','category','url') #tuple is fixed

  #   def __init__(self):
   #      self.list_display
 #admin.site.register(Site)

# Update the registeration to include this customised interface
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
#admin.site.register(Userprofiles) need to have a model for this

# Register your models here.
