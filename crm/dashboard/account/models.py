from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=300, null=True)
    phone = models.CharField(max_length=300, null=True)
    email = models.EmailField(max_length=500, null=True)
    profile_pic = models.ImageField(null=True,default='pic1.webp',blank=True)
    date_created=  models.DateTimeField(auto_now_add=True)

    # for geting the name insted of customer object(1)
    def __str__(self) -> str:
        return self.name
    

    
class Tag(models.Model):
    name = models.CharField(max_length=300, null=True)
    
    def __str__(self) -> str:
        return self.name
    


    
class Product(models.Model):
    CATEGORY= (
         ('Indoor','Indoor'),
         ('Outdoor','Outdoor')
    )
    name=models.CharField(max_length=300, null=True)
    price=models.FloatField(null=True)
    category=models.CharField(max_length=300, null=True,choices=CATEGORY)
    description=models.CharField(max_length=800, null=True)
    date_created=models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag)
    
    def __str__(self) -> str:
        return self.name

    
class Order(models.Model):
        STATUS= (
             ('Pending','Pending'),
             ('out of delivery','out of delivery'),
             ('Delivered','Delivered')
        )
        customer= models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
        product= models.ForeignKey(Product,null=True,on_delete=models.SET_NULL)
        
        date_created=  models.DateTimeField(auto_now_add=True)
        status = models.CharField(max_length=500, null=True,choices=STATUS)
        note  = models.CharField(max_length=1000, null=True)
       
        def __str__(self) -> str:
           
           return self.product.name


