from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin
import nested_admin

class SubCategoryInline(admin.TabularInline, TranslationInlineModelAdmin):
    model = SubCategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    inlines = [SubCategoryInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class ContactInline(nested_admin.NestedTabularInline, TranslationInlineModelAdmin):
    model = Contact
    extra = 1

class AddressInline(nested_admin.NestedTabularInline, TranslationInlineModelAdmin):
    model = Address
    extra = 1

class ProductInline(nested_admin.NestedTabularInline, TranslationInlineModelAdmin):
    model = Product
    extra = 1

class StoreMenuInline(nested_admin.NestedTabularInline, TranslationInlineModelAdmin):
    model = StoreMenu
    extra = 1
    inlines = [ProductInline]

@admin.register(Store)
class AllAdmin(TranslationAdmin, nested_admin.NestedModelAdmin):
    inlines = [ContactInline, AddressInline, StoreMenuInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

admin.site.register(UserProfile)
admin.site.register(Order)
admin.site.register(Courier)
admin.site.register(Review)
admin.site.register(Product)