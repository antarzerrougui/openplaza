from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from .models import Category,Product
from .forms import CategoryModelForm,ProductModelForm


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title',)
    form = CategoryModelForm
    def formfield_for_foreignkey(self,db_field,request,**kwargs):
        if db_field.name == "parent_node_id":
            #print(kwargs['queryset'])
            #print(request)
            pass
        return super(CategoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        pass

class ProductAdmin(admin.ModelAdmin):
    form = ProductModelForm
# Re-register UserAdmin
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)