from django.contrib import admin

from models import Category, UploadFile
from mptt.admin import MPTTModelAdmin


class CategoryMPTTModelAdmin(MPTTModelAdmin):
    # speficfy pixel amount for this ModelAdmin only:
    mptt_level_indent = 12
    #mptt_indent_field = "some_node_field"
    list_display = ['name', 'slug', 'weight', 'active']
    prepopulated_fields = {'slug': ('name',)}
    
        
admin.site.register(Category, CategoryMPTTModelAdmin)

class UploadFileAdmin(admin.ModelAdmin):
    
    def get_category(self, obj):
        return obj.category.name
    
    get_category.short_description = 'Category'
    
    list_display = ['get_category', 'name', 'created', 'active']

admin.site.register(UploadFile, UploadFileAdmin)