from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    phone_number = PhoneNumberField()
    RoleChoices = (
        ('client', 'client'),
        ('owner', 'owner'),
        ('courier', 'courier'),
    )
    role = models.CharField(max_length=20, choices=RoleChoices, default='client')
    date_registered = models.DateField(auto_now_add=True)
    def __str__(self):
        return f'{self.first_name},{self.last_name}'

class Category(models.Model):
    category_name = models.CharField(max_length=25, unique=True)
    category_image = models.ImageField(upload_to='category_photos')
    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategory_category')
    subcategory_name = models.CharField(max_length=25, unique=True)
    subcategory_image = models.ImageField(upload_to='subcategory_photos')


    def __str__(self):
        return self.subcategory_name

class Store(models.Model):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='store_subcategory')
    store_name = models.CharField(max_length=35, unique=True)
    description = models.TextField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store_image = models.ImageField(upload_to='images/')
    created_date = models.DateTimeField(auto_now_add=True)

    def get_average_rating(self):
        ratings = self.review_store.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(), 2)
        return 0

    def get_good_review(self):
        ratings = self.review_store.all()
        total = 0
        if ratings.exists():
            for i in ratings:
                if i.rating > 3:
                  total += 1
            return f'{round(total * 100 / ratings.count())}%'
        return f'{0}%'

    def get_count_people(self):
        ratings = self.review_store.all()
        if ratings.exists():
            if ratings.count() > 500:
                return '500+'
            return ratings.count()




    def __str__(self):
        return self.store_name

class Contact(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_contact')
    contact_name = models.CharField(max_length=20)
    contact_number = PhoneNumberField()

    def __str__(self):
        return f'{self.contact_name}-{self.contact_number}'

class Address(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_address')
    address_name = models.CharField(max_length=50)

    def __str__(self):
        return self.address_name

class StoreMenu(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_menu')
    menu_name = models.CharField(max_length=50, unique=True)


    def __str__(self):
        return self.menu_name

class Product(models.Model):
    store = models.ForeignKey(StoreMenu, on_delete=models.CASCADE, related_name='store_product')
    product_name = models.CharField(max_length=50)
    product_image = models.ImageField(upload_to='product_photos/')
    product_description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=1)
    def __str__(self):
        return self.product_name

class Order(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    StatusChoices = (
        ('pending', 'pending'),
        ('canceled', 'canceled'),
        ('delivered', 'delivered'),
    )
    status = models.CharField(max_length=10, choices=StatusChoices, default='pending')
    delivery_address = models.TextField()
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='order_courier')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.product}'

class Courier(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    current_orders = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='assigned_couriers')
    CourierStatusChoices = (
        ('busy', 'busy'),
        ('avaliable', 'avaliable'),
    )
    courier_status = models.CharField(max_length=20, choices=CourierStatusChoices)
    def __str__(self):
        return f'{self.user},{self.courier_status}'

class Review(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_review')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='review_store')
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_review', null=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.rating}'
