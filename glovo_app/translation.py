from .models import Category, Store, Contact, Address, Product, StoreMenu, SubCategory
from modeltranslation.translator import TranslationOptions,register

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category_name', )

@register(SubCategory)
class SubCategoryTranslationOptions(TranslationOptions):
    fields = ('subcategory_name', )


@register(Store)
class StoreTranslationOptions(TranslationOptions):
    fields = ('store_name', 'description')

@register(Contact)
class ContactTranslationOptions(TranslationOptions):
    fields = ('contact_name', )

@register(Address)
class AddressTranslationOptions(TranslationOptions):
    fields = ('address_name', )

@register(StoreMenu)
class StoreMenuTranslationOptions(TranslationOptions):
    fields = ('menu_name', )

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('product_name', 'product_description')