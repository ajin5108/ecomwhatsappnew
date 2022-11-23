from django.db import models
from versatileimagefield.fields import VersatileImageField
from tinymce.models import HTMLField
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.models import (
    AbstractUser,
 )

# Create your models here.


class Login(AbstractUser):
    is_customer = models.BooleanField(default=False)
    

class Customer(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='user')
    customer_name = models.CharField(max_length = 100,null=True)
    phone_number = models.CharField(default=0, null=True, max_length=10, unique = True)  
    email = models.EmailField(max_length=254,null=True)
    address = models.CharField(max_length = 250)
    
    
class Category(models.Model):
    category = models.CharField(max_length = 200, unique=True)
    image = VersatileImageField(upload_to="categories/", null=True)
    
    def _str_(self):
        return self.category
    
    def get_absolute_url(self):
        return reverse_lazy("user:shop", kwargs={"id": self.id})
    
    def get_subcategories(self):
        return SubCategory.objects.filter(category=self) 
         

    
    
class SubCategory(models.Model):
    subcategory = models.CharField(max_length = 150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy("user:product", kwargs={"id": self.id})

    def get_shop_url(self):
        return reverse_lazy("user:shop", kwargs={"id": self.id})
    
    def get_products(self):
        return Product.objects.filter(subcategory=self) 
    
    def _str_(self):
        return self.subcategory
       

    
class Product(models.Model):
    # user=models.ForeignKey(Customer, on_delete=models.CASCADE, null=True,default='')
    product = models.CharField(max_length = 150)
    image = VersatileImageField(upload_to="products/", null=True)
    sub_image1 = VersatileImageField(upload_to="products/", null=True)
    sub_image2 = VersatileImageField(upload_to="products/", null=True)
    sub_image3 = VersatileImageField(upload_to="products/", null=True)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    price = models.IntegerField()
    offer_price = models.IntegerField(null = True)
    quantity = models.IntegerField(default = 0)
    description = models.CharField(max_length = 250)
    is_top_save_today= models.BooleanField(default = False)
    is_best_seller = models.BooleanField(default = False)
        
    def _str_(self):
        return self.product
    

class MainBanner(models.Model):
    bannerbig = VersatileImageField(upload_to="MainBanner/", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    

class SubBanners1(models.Model):
    subbanner1 = VersatileImageField(upload_to="SubBanners/", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
    
class SubBanners2(models.Model):
    subbanner2 = VersatileImageField(upload_to="SubBanners/", null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    


class HeaderFlash(models.Model):
    address =  models.CharField(max_length = 150)
    offer_product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    
    def _str_(self):
        return self.address

class AddToCart(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True,default='')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    quantity=models.IntegerField(null=True, default=1 )
    total = models.IntegerField(null=True)
    # def get_products(self):
    #     return Product.objects.all() 


    def _str_(self):
        return self.product
    
    
class Cart(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True,default='')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    product_qty=models.IntegerField(null=False,blank=False)
    added_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.product
    
     
class Wishlist(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True,default='')
    product = models.ForeignKey(Product,on_delete=models.CASCADE,default='',null=True,blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    
    # def get_products(self):
    #     return Product.objects.filter(product=self) 
    


class ChangePassword(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE, blank=True, null=True)
    forgot_password_token = models.CharField(max_length=100)
    created_at = models. DateTimeField(auto_now_add = True)
    status = models.BooleanField(default=False)

    def str(self):
        return str(self.user)
 
    
def get_absolute_url(self):
    return reverse("_detail", kwargs={"pk": self.pk})